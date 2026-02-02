# DataInsight Pro - Working Version
import os
import csv
from datetime import datetime
from pathlib import Path


class DataPoint:
    def __init__(self, date, value, category, region):
        self.date = date
        self.value = float(value)
        self.category = category
        self.region = region


class DataLoader:
    def load_csv(self, file_path):
        data_points = []
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    dp = DataPoint(
                        date=row.get('date', ''),
                        value=float(row.get('sales', row.get('value', 0))),
                        category=row.get('category', row.get('product', '')),
                        region=row.get('region', '')
                    )
                    data_points.append(dp)
                except (ValueError, KeyError) as e:
                    print(f"Warning: Skip row {row}, error {e}")
                    continue
        return data_points

    def get_info(self, data_points):
        if not data_points:
            return {'error': 'Empty dataset'}
        
        categories = set(dp.category for dp in data_points)
        regions = set(dp.region for dp in data_points)
        values = [dp.value for dp in data_points]
        
        return {
            'total_records': len(data_points),
            'date_range': {
                'start': data_points[0].date,
                'end': data_points[-1].date
            },
            'categories': sorted(categories),
            'regions': sorted(regions),
            'total_value': sum(values),
            'avg_value': sum(values) / len(values),
            'min_value': min(values),
            'max_value': max(values)
        }


class DataAnalyzer:
    def calculate_statistics(self, data_points):
        values = [dp.value for dp in data_points]
        n = len(values)
        mean = sum(values) / n
        
        variance = sum((x - mean) ** 2 for x in values) / n
        std = variance ** 0.5
        
        return {
            'total_value': sum(values),
            'avg_value': mean,
            'min_value': min(values),
            'max_value': max(values),
            'median_value': sorted(values)[n // 2],
            'std_value': std
        }

    def analyze_by_category(self, data_points):
        category_stats = {}
        for dp in data_points:
            if dp.category not in category_stats:
                category_stats[dp.category] = {'count': 0, 'total': 0}
            category_stats[dp.category]['count'] += 1
            category_stats[dp.category]['total'] += dp.value
        
        for cat in category_stats:
            category_stats[cat]['avg'] = category_stats[cat]['total'] / category_stats[cat]['count']
        
        sorted_cats = sorted(category_stats.items(), key=lambda x: x[1]['total'], reverse=True)
        return dict(sorted_cats)

    def analyze_by_region(self, data_points):
        region_stats = {}
        for dp in data_points:
            if dp.region not in region_stats:
                region_stats[dp.region] = {'count': 0, 'total': 0}
            region_stats[dp.region]['count'] += 1
            region_stats[dp.region]['total'] += dp.value
        
        for reg in region_stats:
            region_stats[reg]['avg'] = region_stats[reg]['total'] / region_stats[reg]['count']
        
        sorted_regs = sorted(region_stats.items(), key=lambda x: x[1]['total'], reverse=True)
        return dict(sorted_regs)

    def detect_anomalies(self, data_points, threshold=2.0):
        values = [dp.value for dp in data_points]
        mean = sum(values) / len(values)
        std = (sum((x - mean) ** 2 for x in values) / len(values)) ** 0.5
        
        anomalies = []
        for i, dp in enumerate(data_points):
            z_score = (dp.value - mean) / std if std > 0 else 0
            if abs(z_score) > threshold:
                anomalies.append({
                    'date': dp.date,
                    'value': dp.value,
                    'z_score': round(z_score, 2)
                })
        return anomalies

    def calculate_growth_rate(self, data_points):
        if len(data_points) < 2:
            return {'error': 'Not enough data'}
        
        growth_rates = []
        for i in range(1, len(data_points)):
            if data_points[i-1].value > 0:
                rate = (data_points[i].value - data_points[i-1].value) / data_points[i-1].value * 100
                growth_rates.append({
                    'date': data_points[i].date,
                    'growth_rate': round(rate, 2)
                })
        
        if growth_rates:
            avg_growth = sum(gr['growth_rate'] for gr in growth_rates) / len(growth_rates)
            return {
                'growth_rates': growth_rates,
                'average_growth': round(avg_growth, 2),
                'trend': 'increasing' if avg_growth > 0 else 'decreasing' if avg_growth < 0 else 'stable'
            }
        return {'error': 'No growth data'}


class ReportGenerator:
    def generate_markdown(self, result):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = f"""# Data Analysis Report

Generated at: {timestamp}
System: DataInsight Pro v1.0

---

## Executive Summary

{result.get('summary', 'No summary')}

---

## Data Overview

Total Records: {result.get('total_records', 0)}
Date Range: {result.get('date_range', {}).get('start', 'Unknown')} to {result.get('date_range', {}).get('end', 'Unknown')}

---

## Key Metrics

Total Value: {self._format_number(result.get('total_value', 0))}
Average Value: {self._format_number(result.get('avg_value', 0))}
Min Value: {self._format_number(result.get('min_value', 0))}
Max Value: {self._format_number(result.get('max_value', 0))}
Median Value: {self._format_number(result.get('median_value', 0))}
Std Value: {self._format_number(result.get('std_value', 0))}

---

## Findings

{self._format_findings(result.get('findings', []))}

---

## Trend Analysis

Trend: {result.get('trend', 'Unknown')}
Average Growth: {result.get('average_growth', 0)}%

---

## Category Analysis

{self._format_category_analysis(result.get('category_analysis', {}))}

---

## Region Analysis

{self._format_region_analysis(result.get('region_analysis', {}))}

---

## Anomalies Detected

{self._format_anomalies(result.get('anomaly_count', 0), result.get('anomalies', []))}

---

## Recommendations

{self._format_recommendations(result.get('recommendations', []))}

---

*Report generated by DataInsight Pro*
"""
        return report

    def _format_number(self, num):
        return "{:,.2f}".format(num) if isinstance(num, float) else "{:,}".format(int(num))

    def _format_findings(self, findings):
        if not findings:
            return "No key findings"
        lines = []
        for i, finding in enumerate(findings, 1):
            lines.append(f"{i}. {finding}")
        return "\n".join(lines)

    def _format_category_analysis(self, cat_analysis):
        if not cat_analysis:
            return "No category analysis"
        lines = []
        for cat, stats in cat_analysis.items():
            lines.append(f"- **{cat}**: Total: {self._format_number(stats['total'])}, Avg: {self._format_number(stats['avg'])}")
        return "\n".join(lines)

    def _format_region_analysis(self, reg_analysis):
        if not reg_analysis:
            return "No region analysis"
        lines = []
        for reg, stats in reg_analysis.items():
            lines.append(f"- **{reg}**: Total: {self._format_number(stats['total'])}, Avg: {self._format_number(stats['avg'])}")
        return "\n".join(lines)

    def _format_anomalies(self, count, anomalies):
        if count == 0:
            return "No anomalies detected"
        lines = [f"Detected {count} anomalies:"]
        for a in anomalies:
            lines.append(f"  - {a['date']}: {self._format_number(a['value'])} (z-score: {a['z_score']})")
        return "\n".join(lines)

    def _format_recommendations(self, recommendations):
        if not recommendations:
            return "No specific recommendations"
        lines = []
        for i, rec in enumerate(recommendations, 1):
            lines.append(f"{i}. {rec}")
        return "\n".join(lines)

    def save_report(self, report, output_path):
        try:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
            
            print(f"Report saved to: {output_file.absolute()}")
            return True
        except Exception as e:
            print(f"Error saving report: {e}")
            return False


class DataAnalysisEngine:
    def __init__(self):
        self.loader = DataLoader()
        self.analyzer = DataAnalyzer()
        self.reporter = ReportGenerator()

    def analyze(self, goal, dataset_path, depth="standard"):
        print(f"\nStarting analysis...")
        print(f"Goal: {goal}")
        print(f"Dataset: {dataset_path}")
        print(f"Depth: {depth}")

        # Load data
        print("\n[1/5] Loading data...")
        data_points = self.loader.load_csv(dataset_path)
        print(f"   Loaded {len(data_points)} records")

        # Data exploration
        print("\n[2/5] Data exploration...")
        data_info = self.loader.get_info(data_points)
        print(f"   Date range: {data_info['date_range']['start']} to {data_info['date_range']['end']}")
        print(f"   Categories: {', '.join(data_info['categories'])}")
        print(f"   Regions: {', '.join(data_info['regions'])}")

        # Statistical analysis
        print("\n[3/5] Statistical analysis...")
        stats = self.analyzer.calculate_statistics(data_points)
        category_analysis = self.analyzer.analyze_by_category(data_points)
        region_analysis = self.analyzer.analyze_by_region(data_points)
        anomalies = self.analyzer.detect_anomalies(data_points)
        growth_analysis = self.analyzer.calculate_growth_rate(data_points)

        print(f"   Total value: {self.reporter._format_number(stats['total_value'])}")
        print(f"   Avg value: {self.reporter._format_number(stats['avg_value'])}")
        print(f"   Anomalies: {len(anomalies)}")

        # Generate insights
        print("\n[4/5] Generating insights...")
        findings = self._generate_findings(stats, category_analysis, region_analysis, anomalies, growth_analysis)
        recommendations = self._generate_recommendations(findings, growth_analysis)

        # Generate summary
        print("\n[5/5] Generating report...")
        summary = f"""Analysis goal: {goal}
Dataset: {dataset_path}
Key metrics:
- Total value: {self.reporter._format_number(stats['total_value'])}
- Trend: {growth_analysis.get('trend', 'Unknown')}
"""

        result = {
            'summary': summary,
            'total_records': len(data_points),
            'date_range': data_info.get('date_range', {}),
            'total_value': stats['total_value'],
            'avg_value': stats['avg_value'],
            'min_value': stats['min_value'],
            'max_value': stats['max_value'],
            'median_value': stats['median_value'],
            'std_value': stats['std_value'],
            'findings': findings,
            'recommendations': recommendations,
            'trend': growth_analysis.get('trend', 'Unknown'),
            'average_growth': growth_analysis.get('average_growth', 0),
            'category_analysis': category_analysis,
            'region_analysis': region_analysis,
            'anomalies': anomalies,
            'anomaly_count': len(anomalies),
            'growth_analysis': growth_analysis
        }

        print("\nAnalysis complete!")
        return result

    def _generate_findings(self, stats, category_analysis, region_analysis, anomalies, growth_analysis):
        findings = []
        
        findings.append(f"Total value: {self.reporter._format_number(stats['total_value'])}")
        
        if category_analysis:
            top_cat = list(category_analysis.keys())[0]
            findings.append(f"Top category: {top_cat}")
        
        if region_analysis:
            top_reg = list(region_analysis.keys())[0]
            findings.append(f"Core region: {top_reg}")
        
        findings.append(f"Overall trend: {growth_analysis.get('trend', 'Unknown')}")
        
        if anomalies:
            findings.append(f"Detected {len(anomalies)} anomalies")
        
        return findings

    def _generate_recommendations(self, findings, growth_analysis):
        recommendations = []
        
        trend = growth_analysis.get('trend', 'stable')
        
        if trend == 'increasing':
            recommendations.append('Maintain current strategy and consider scaling up')
        elif trend == 'decreasing':
            recommendations.append('Investigate decline and adjust strategy')
        else:
            recommendations.append('Stable period is a good time to optimize operations')
        
        if anomalies:
            recommendations.append('Deep dive into anomaly causes')
        
        recommendations.append('Monitor key metrics regularly')
        recommendations.append('Focus investment on top performers')
        
        return recommendations


if __name__ == '__main__':
    print("=" * 60)
    print("DataInsight Pro - Working Version")
    print("=" * 60)

    engine = DataAnalysisEngine()

    result = engine.analyze(
        goal="Analyze sales data trends and anomalies",
        dataset_path="data/samples/sales_2024_Q1.csv",
        depth="standard"
    )

    print("\nGenerating report...")
    report = engine.reporter.generate_markdown(result)
    print(report)

    print("\nSaving report...")
    engine.reporter.save_report(report, "final_report.md")

    print("\nDemo complete!")
