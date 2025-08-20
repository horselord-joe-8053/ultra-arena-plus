#!/bin/bash

# 🚀 Simple Ultra Arena API Test - Process Files
# Just sends request and shows result with emojis!

BASE_URL="http://localhost:5002"
ENDPOINT="/api/process"
FULL_URL="${BASE_URL}${ENDPOINT}"

# Test data paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INPUT_PATH="${SCRIPT_DIR}/../test_input_files_2/1_file"

echo "🚀 Starting Simple API Test..."
echo "📍 Testing: $FULL_URL"
echo "📁 Input: $INPUT_PATH"
echo ""

# Check if input exists
if [ ! -d "$INPUT_PATH" ]; then
    echo "❌ Error: Input directory not found!"
    exit 1
fi

echo "📤 Sending request..."
echo ""

json_data=$(cat <<EOF
{
  "input_path": "$INPUT_PATH"
}
EOF
)

response=$(curl -s -w "\n%{http_code}" -X POST "${FULL_URL}" \
  -H "Content-Type: application/json" \
  -d "$json_data")

http_code=$(echo "$response" | tail -n1)
response_body=$(echo "$response" | sed '$d')

echo "📥 Response received!"
echo "🔢 Status Code: $http_code"
echo "📄 Response:"
echo "$response_body" | python3 -m json.tool 2>/dev/null || echo "$response_body"
echo ""

if [ "$http_code" -eq 200 ]; then
    echo "✅ SUCCESS! Request worked!"
else
    echo "❌ FAILED! Status code: $http_code"
fi

echo ""
echo "�� Test completed!" 