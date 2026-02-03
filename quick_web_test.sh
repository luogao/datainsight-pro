#!/bin/bash

# 快速测试 Web UI 数据流
echo "================================"
echo "Web UI 数据流测试"
echo "================================"
echo ""

# 1. 测试后端健康状态
echo "1️⃣  测试后端健康状态..."
HEALTH=$(curl -s http://localhost:8000/health)
if echo "$HEALTH" | grep -q "healthy"; then
    echo "✅ 后端服务正常"
else
    echo "❌ 后端服务异常"
    echo "$HEALTH"
    exit 1
fi
echo ""

# 2. 获取示例数据
echo "2️⃣  获取示例数据列表..."
SAMPLES=$(curl -s http://localhost:8000/sample-data)
echo "$SAMPLES" | python -m json.tool 2>/dev/null || echo "$SAMPLES"
echo ""

# 3. 如果有示例数据，测试上传
echo "3️⃣  测试文件上传功能..."
# 查找第一个 CSV 文件
SAMPLE_FILE=$(find . -name "*.csv" -type f | head -1)

if [ -n "$SAMPLE_FILE" ]; then
    echo "找到示例文件: $SAMPLE_FILE"
    UPLOAD_RESULT=$(curl -s -X POST http://localhost:8000/upload \
        -F "file=@$SAMPLE_FILE")

    echo "$UPLOAD_RESULT" | python -m json.tool 2>/dev/null || echo "$UPLOAD_RESULT"

    # 提取文件路径
    FILE_PATH=$(echo "$UPLOAD_RESULT" | python -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(data.get('file_path', ''))
except:
    pass
" 2>/dev/null)

    if [ -n "$FILE_PATH" ]; then
        echo ""
        echo "4️⃣  启动分析任务..."
        ANALYZE_RESULT=$(curl -s -X POST http://localhost:8000/analyze \
            -F "goal=分析数据趋势" \
            -F "dataset_path=$FILE_PATH" \
            -F "depth=standard" \
            -F "output_format=markdown")

        echo "$ANALYZE_RESULT" | python -m json.tool 2>/dev/null || echo "$ANALYZE_RESULT"

        # 提取 task_id
        TASK_ID=$(echo "$ANALYZE_RESULT" | python -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(data.get('task_id', ''))
except:
    pass
" 2>/dev/null)

        if [ -n "$TASK_ID" ]; then
            echo ""
            echo "5️⃣  任务已创建！Task ID: $TASK_ID"
            echo "查看任务状态："
            echo "curl http://localhost:8000/tasks/$TASK_ID"
            echo ""
            echo "等待 10 秒后检查状态..."
            sleep 10

            TASK_STATUS=$(curl -s http://localhost:8000/tasks/$TASK_ID)
            echo "$TASK_STATUS" | python -m json.tool 2>/dev/null || echo "$TASK_STATUS"
        fi
    fi
else
    echo "⚠️  未找到 CSV 示例文件"
fi

echo ""
echo "================================"
echo "✅ 测试完成"
echo "================================"
echo ""
echo "前端地址: http://localhost:3000"
echo "API 文档: http://localhost:8000/docs"
