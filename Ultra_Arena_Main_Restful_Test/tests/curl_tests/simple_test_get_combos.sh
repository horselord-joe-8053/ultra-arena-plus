#!/bin/bash

# 🚀 Simple Ultra Arena API Test - Get Combos
# Just gets available combos with emojis!

BASE_URL="http://localhost:5002"
ENDPOINT="/api/combos"
FULL_URL="${BASE_URL}${ENDPOINT}"

echo "🚀 Starting Get Combos Test..."
echo "📍 Testing: $FULL_URL"
echo ""

echo "📤 Sending GET request..."
echo ""

response=$(curl -s -w "\n%{http_code}" -X GET "${FULL_URL}")

http_code=$(echo "$response" | tail -n1)
response_body=$(echo "$response" | sed '$d')

echo "📥 Response received!"
echo "🔢 Status Code: $http_code"
echo "📄 Response:"
echo "$response_body" | python3 -m json.tool 2>/dev/null || echo "$response_body"
echo ""

if [ "$http_code" -eq 200 ]; then
    echo "✅ SUCCESS! Got combos!"
else
    echo "❌ FAILED! Status code: $http_code"
fi

echo ""
echo "🎉 Get combos test completed!" 