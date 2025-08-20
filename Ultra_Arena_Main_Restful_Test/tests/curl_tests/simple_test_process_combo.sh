#!/bin/bash

# 🚀 Simple Ultra Arena API Test - Process Combo
# Just sends combo request and shows result with emojis!

BASE_URL="http://localhost:5002"
ENDPOINT="/api/process/combo"
FULL_URL="${BASE_URL}${ENDPOINT}"

# Test profile configuration
TEST_PROFILE="default_profile"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEST_PROFILES_DIR="${SCRIPT_DIR}/../../test_profiles"
INPUT_DIR="${TEST_PROFILES_DIR}/${TEST_PROFILE}/input_files"
OUTPUT_DIR="${TEST_PROFILES_DIR}/${TEST_PROFILE}/output_files"

echo "🚀 Starting Process Combo Test..."
echo "📍 Testing: $FULL_URL"
echo ""

echo "📤 Sending request..."
echo ""

json_data=$(cat <<EOF
{
          "combo_name": "combo_test_8_strategies",
  "input_pdf_dir_path": "${INPUT_DIR}",
  "run_config": {
    "run_type": "normal",
    "output_dir": "${OUTPUT_DIR}"
  },
  "streaming": false,
  "max_cc_strategies": 3,
  "max_cc_filegroups": 5
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
    echo "✅ SUCCESS! Combo processing worked!"
else
    echo "❌ FAILED! Status code: $http_code"
fi

echo ""
echo "🎉 Process combo test completed!" 