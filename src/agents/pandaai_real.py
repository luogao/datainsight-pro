"""
PandaAI Agent - 真正集成 pandasai 库
负责：提供高级 AI 洞察、智能问答、数据可视化、数据清洗
"""
import os
import pandas as pd
from typing import Dict, List, Any, Optional
from crewai import Agent
from crewai.tools import tool
from dotenv import load_dotenv

load_dotenv()


# ========================================
# PandaAI 真实集成
# ========================================

try:
    # pandasai 2.x 使用 SmartDataframe
    from pandasai import SmartDataframe
    # 尝试导入 LLM 配置（新版可能位置不同）
    try:
        from pandasai.llm import OpenAI
    except ImportError:
        # 新版本可能在不同的位置
        from langchain_community.llms import OpenAI as LangchainOpenAI
        OpenAI = LangchainOpenAI
    PANDAAI_AVAILABLE = True
except ImportError:
    PANDAAI_AVAILABLE = False
    print("⚠️  pandasai 未安装或版本不兼容。请运行: pip install pandasai")


class RealPandaAI:
    """真正的 PandaAI 集成 (支持 pandasai 2.x)"""

    def __init__(self):
        if not PANDAAI_AVAILABLE:
            raise ImportError("pandasai 未安装，请运行: pip install pandasai")

        # 初始化 LLM 配置
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4")

        if not self.api_key:
            raise ValueError("需要设置 OPENAI_API_KEY 环境变量")

        # 配置环境变量（pandasai 使用）
        os.environ["OPENAI_API_KEY"] = self.api_key
        if self.base_url and self.base_url != "https://api.openai.com/v1":
            os.environ["OPENAI_API_BASE"] = self.base_url

        # 尝试创建 PandaAI LLM 实例
        try:
            from pandasai.llm import OpenAI
            # PandaAI 的 OpenAI 类参数
            llm_kwargs = {"api_key": self.api_key}
            # 只有标准 OpenAI 才传递 api_key，自定义端点使用环境变量
            if self.base_url and self.base_url != "https://api.openai.com/v1":
                # 使用环境变量配置自定义端点
                self.llm = None
            else:
                self.llm = OpenAI(**llm_kwargs)
        except Exception as e:
            # 如果创建失败，使用环境变量方式
            print(f"⚠️  PandaAI LLM 创建失败: {e}，将使用环境变量")
            self.llm = None

    def chat(self, df: pd.DataFrame, question: str) -> str:
        """
        使用 PandaAI 进行智能问答

        Args:
            df: DataFrame
            question: 自然语言问题

        Returns:
            PandaAI 的回答
        """
        try:
            # 使用 SmartDataframe (pandasai 2.x)
            if self.llm:
                from pandasai.schemas.df_config import Config
                config = Config(llm=self.llm)
                sdf = SmartDataframe(df, config=config)
            else:
                # 使用环境变量配置
                sdf = SmartDataframe(df)
            result = sdf.chat(question)
            return str(result)
        except Exception as e:
            return f"❌ PandaAI 查询失败: {str(e)}"

    def generate_chart(self, df: pd.DataFrame, chart_type: str, config: Dict = None) -> Dict:
        """
        生成图表配置

        Args:
            df: DataFrame
            chart_type: 图表类型 (line, bar, scatter, pie)
            config: 图表配置

        Returns:
            图表配置字典
        """
        chart_prompts = {
            "line": "生成一个折线图，展示时间序列趋势",
            "bar": "生成一个柱状图，比较不同类别的数值",
            "scatter": "生成一个散点图，展示两个变量的关系",
            "pie": "生成一个饼图，展示各类别的占比"
        }

        prompt = chart_prompts.get(chart_type, f"生成一个{chart_type}图表")

        try:
            # 使用 SmartDataframe 生成图表
            sdf = SmartDataframe(df)
            result = sdf.chat(prompt)
            return {
                "type": chart_type,
                "prompt": prompt,
                "result": str(result),
                "success": True
            }
        except Exception as e:
            return {
                "type": chart_type,
                "error": str(e),
                "success": False
            }

    def clean_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        智能数据清洗

        Args:
            df: DataFrame

        Returns:
            清洗后的数据和清洗报告
        """
        try:
            # 获取原始信息
            original_shape = df.shape
            original_nulls = df.isnull().sum().sum()

            # 使用 PandaAI 清洗数据
            prompt = "请清洗这个数据集：处理缺失值、去除重复值、纠正异常值"
            sdf = SmartDataframe(df)
            result = sdf.chat(prompt)

            # 如果返回的是 DataFrame
            if isinstance(result, pd.DataFrame):
                cleaned_df = result
            else:
                # 否则返回原始 DataFrame
                cleaned_df = df.drop_duplicates()

            cleaned_shape = cleaned_df.shape
            cleaned_nulls = cleaned_df.isnull().sum().sum()

            return {
                "original_rows": original_shape[0],
                "cleaned_rows": cleaned_shape[0],
                "removed_rows": original_shape[0] - cleaned_shape[0],
                "original_nulls": int(original_nulls),
                "cleaned_nulls": int(cleaned_nulls),
                "cleaned_df": cleaned_df,
                "report": str(result)
            }
        except Exception as e:
            return {
                "error": str(e),
                "cleaned_df": df
            }

    def analyze_patterns(self, df: pd.DataFrame) -> List[str]:
        """
        分析数据模式和异常

        Args:
            df: DataFrame

        Returns:
            洞察列表
        """
        insights = []

        try:
            # 创建 SmartDataframe
            sdf = SmartDataframe(df)

            # 1. 数据概览洞察
            prompt = "分析这个数据集的整体特征，包括：数据分布、异常值、相关性"
            overview = sdf.chat(prompt)
            insights.append(f"📊 数据概览：{overview}")

            # 2. 趋势分析
            prompt = "识别数据中的趋势模式和周期性"
            trends = sdf.chat(prompt)
            insights.append(f"📈 趋势分析：{trends}")

            # 3. 异常检测
            prompt = "检测数据中的异常值和离群点，并解释可能的原因"
            anomalies = sdf.chat(prompt)
            insights.append(f"🔍 异常检测：{anomalies}")

            # 4. 相关性分析
            if df.shape[1] > 1:
                prompt = "分析变量之间的相关性，找出强相关关系"
                correlations = sdf.chat(prompt)
                insights.append(f"🔗 相关性分析：{correlations}")

        except Exception as e:
            insights.append(f"❌ 分析失败：{str(e)}")

        return insights

    def predict_future(self, df: pd.DataFrame, periods: int = 3) -> Dict[str, Any]:
        """
        预测未来趋势

        Args:
            df: DataFrame (历史数据)
            periods: 预测周期数

        Returns:
            预测结果
        """
        try:
            prompt = f"基于这个数据集的历史数据，预测未来 {periods} 个周期的趋势，包括预测值和置信区间"
            sdf = SmartDataframe(df)
            result = sdf.chat(prompt)

            return {
                "periods": periods,
                "prediction": str(result),
                "success": True
            }
        except Exception as e:
            return {
                "periods": periods,
                "error": str(e),
                "success": False
            }

    def get_data_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        获取数据集摘要信息

        Args:
            df: DataFrame

        Returns:
            数据摘要
        """
        try:
            prompt = "请生成这个数据集的详细摘要，包括：统计特征、数据类型、质量评估"
            sdf = SmartDataframe(df)
            result = sdf.chat(prompt)

            return {
                "shape": df.shape,
                "columns": list(df.columns),
                "dtypes": df.dtypes.to_dict(),
                "summary": str(result),
                "basic_stats": df.describe().to_dict() if df.shape[1] > 0 else {}
            }
        except Exception as e:
            return {
                "error": str(e),
                "shape": df.shape,
                "columns": list(df.columns)
            }


# 全局 PandaAI 实例
_pandaai_instance: Optional[RealPandaAI] = None


def get_pandaai() -> RealPandaAI:
    """获取 PandaAI 实例（单例模式）"""
    global _pandaai_instance
    if _pandaai_instance is None:
        _pandaai_instance = RealPandaAI()
    return _pandaai_instance


# ========================================
# CrewAI Tools (使用真实的 PandaAI)
# ========================================

@tool
def pandaai_chat(question: str, file_path: str) -> str:
    """
    使用 PandaAI 进行智能数据分析问答

    Args:
        question: 自然语言问题
        file_path: 数据文件路径

    Returns:
        PandaAI 的回答
    """
    if not PANDAAI_AVAILABLE:
        return "⚠️  pandasai 未安装，无法使用此功能。请运行: pip install pandasai"

    try:
        # 直接从文件读取数据，避免将全量数据放入 prompt
        df = pd.read_csv(file_path)

        if df.empty:
            return "❌ 数据为空"

        pandaai = get_pandaai()
        result = pandaai.chat(df, question)
        return result

    except Exception as e:
        return f"❌ PandaAI 问答失败: {str(e)}"


@tool
def pandaai_clean_data(file_path: str) -> str:
    """
    使用 PandaAI 智能清洗数据

    Args:
        file_path: 数据文件路径

    Returns:
        清洗报告
    """
    if not PANDAAI_AVAILABLE:
        return "⚠️  pandasai 未安装"

    try:
        df = pd.read_csv(file_path)
        pandaai = get_pandaai()
        result = pandaai.clean_data(df)

        return f"""✅ 数据清洗完成
- 原始行数：{result.get('original_rows', 0)}
- 清洗后行数：{result.get('cleaned_rows', 0)}
- 删除重复行：{result.get('removed_rows', 0)}
- 缺失值处理：{result.get('original_nulls', 0)} → {result.get('cleaned_nulls', 0)}
- 清洗报告：{result.get('report', 'N/A')[:200]}..."""
    except Exception as e:
        return f"❌ 数据清洗失败: {str(e)}"


@tool
def pandaai_analyze_patterns(file_path: str) -> str:
    """
    使用 PandaAI 分析数据模式和洞察

    Args:
        file_path: 数据文件路径

    Returns:
        分析洞察
    """
    if not PANDAAI_AVAILABLE:
        return "⚠️  pandasai 未安装"

    try:
        df = pd.read_csv(file_path)
        pandaai = get_pandaai()
        insights = pandaai.analyze_patterns(df)

        return "\n\n".join(insights)
    except Exception as e:
        return f"❌ 模式分析失败: {str(e)}"


@tool
def pandaai_predict_trend(file_path: str, periods: int = 3) -> str:
    """
    使用 PandaAI 预测未来趋势

    Args:
        file_path: 数据文件路径
        periods: 预测周期数

    Returns:
        趋势预测结果
    """
    if not PANDAAI_AVAILABLE:
        return "⚠️  pandasai 未安装"

    try:
        df = pd.read_csv(file_path)
        pandaai = get_pandaai()
        prediction = pandaai.predict_future(df, periods)

        if prediction.get('success'):
            return f"""📈 PandaAI 趋势预测
预测周期：{periods}
预测结果：
{prediction.get('prediction', 'N/A')[:500]}..."""
        else:
            return f"❌ 预测失败：{prediction.get('error', 'Unknown error')}"
    except Exception as e:
        return f"❌ 趋势预测失败: {str(e)}"


@tool
def pandaai_generate_chart(file_path: str, chart_type: str = "line") -> str:
    """
    使用 PandaAI 生成数据可视化图表

    Args:
        file_path: 数据文件路径
        chart_type: 图表类型 (line, bar, scatter, pie)

    Returns:
        图表生成结果
    """
    if not PANDAAI_AVAILABLE:
        return "⚠️  pandasai 未安装"

    try:
        df = pd.read_csv(file_path)
        pandaai = get_pandaai()
        chart = pandaai.generate_chart(df, chart_type)

        if chart.get('success'):
            return f"""📊 图表生成成功
类型：{chart_type}
结果：{chart.get('result', 'N/A')[:500]}..."""
        else:
            return f"❌ 图表生成失败：{chart.get('error', 'Unknown error')}"
    except Exception as e:
        return f"❌ 图表生成失败: {str(e)}"


@tool
def pandaai_data_summary(file_path: str) -> str:
    """
    使用 PandaAI 生成数据摘要

    Args:
        file_path: 数据文件路径

    Returns:
        数据摘要
    """
    if not PANDAAI_AVAILABLE:
        return "⚠️  pandasai 未安装"

    try:
        df = pd.read_csv(file_path)
        pandaai = get_pandaai()
        summary = pandaai.get_data_summary(df)

        return f"""📊 PandaAI 数据摘要
数据规模：{summary.get('shape', 'Unknown')}
字段列表：{', '.join(summary.get('columns', []))}
摘要信息：
{summary.get('summary', 'N/A')[:500]}..."""
        """
    except Exception as e:
        return f"❌ 摘要生成失败: {str(e)}"


# ========================================
# PandaAI Agent (CrewAI)
# ========================================

def create_pandaai_agent():
    """创建 PandaAI Agent (支持自定义 LLM 配置)"""
    # 获取 LLM 配置
    from langchain_openai import ChatOpenAI

    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")
    model = os.getenv("OPENAI_MODEL", "gpt-4")

    if not api_key:
        raise ValueError("需要设置 OPENAI_API_KEY 环境变量")

    # 创建 LLM（支持自定义 base_url）
    llm_kwargs = {
        "model": model,
        "temperature": 0.7,
        "max_tokens": 4096
    }

    if base_url:
        llm_kwargs["base_url"] = base_url

    llm = ChatOpenAI(
        api_key=api_key,
        **llm_kwargs
    )

    # 创建 Agent
    pandaai_agent = Agent(
        role="AI 数据洞察专家（PandaAI 集成）",
        goal="利用 PandaAI 提供高级数据分析、智能问答、数据可视化和预测",
        backstory="""你是一位经验丰富的 AI 数据科学家，专门使用 PandaAI 进行高级数据分析。

        你能够：
        - 使用 PandaAI 进行自然语言数据查询
        - 生成智能数据可视化图表
        - 进行数据清洗和预处理
        - 识别数据模式和异常
        - 预测未来趋势
        - 提供可执行的业务洞察

        你总是能够从数据中发现别人看不到的模式，并将其转化为实际行动建议。
        你的分析既有数据支撑，又具有战略眼光。""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[
            pandaai_chat,
            pandaai_clean_data,
            pandaai_analyze_patterns,
            pandaai_predict_trend,
            pandaai_generate_chart,
            pandaai_data_summary
        ]
    )

    return pandaai_agent


# 导出 Agent
pandaai_agent = create_pandaai_agent()
