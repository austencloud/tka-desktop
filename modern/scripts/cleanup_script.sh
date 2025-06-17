#!/bin/bash
# TKA Desktop Modern - Cleanup Script
# Implements the high-priority cleanup recommendations

echo "🧹 TKA Desktop Modern Cleanup Script"
echo "====================================="

# Change to modern directory (parent of scripts)
cd "$(dirname "$0")/.."

echo "📂 Current directory: $(pwd)"

# 1. Create demos directory if it doesn't exist
echo "📦 Creating tests/demos directory..."
mkdir -p tests/demos

# 2. Move demo files (with error handling)
echo "🎨 Moving demo files to tests/demos/..."

if [ -f "demo_animated_backgrounds.py" ]; then
    mv demo_animated_backgrounds.py tests/demos/
    echo "   ✅ Moved demo_animated_backgrounds.py"
else
    echo "   ℹ️  demo_animated_backgrounds.py already moved or not found"
fi

if [ -f "example_background_usage.py" ]; then
    mv example_background_usage.py tests/demos/
    echo "   ✅ Moved example_background_usage.py"
else
    echo "   ℹ️  example_background_usage.py already moved or not found"
fi

# 3. Report status
echo ""
echo "📊 Cleanup Status:"
echo "   ✅ High-priority cleanup complete"
echo "   📁 Demo files organized in tests/demos/"
echo ""

# 4. List files that need review
echo "🔍 Files requiring manual review:"
echo ""
echo "   Debug files in tests/:"
ls -1 tests/debug_*.py 2>/dev/null | sed 's/^/      /' || echo "      No debug files found"
echo ""

echo "   Fix-specific tests in tests/:"
ls -1 tests/test_*_fix.py 2>/dev/null | sed 's/^/      /' || echo "      No fix tests found"
echo ""

echo "   Wrapper file:"
if [ -f "construct_tab.py" ]; then
    echo "      construct_tab.py (review if still needed)"
else
    echo "      No wrapper files found"
fi

echo ""
echo "📋 Next steps:"
echo "   1. Review debug files for continued relevance"
echo "   2. Review fix-specific tests for obsolescence" 
echo "   3. Decide fate of construct_tab.py"
echo "   4. Test application: python main.py"
echo ""
echo "✅ Cleanup script complete!"
