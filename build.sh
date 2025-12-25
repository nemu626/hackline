#!/bin/bash
#
# HackLine Font Build Script
# Usage: ./build.sh [--nerd]
#

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}============================================================${NC}"
echo -e "${GREEN}HackLine Font Build Script${NC}"
echo -e "${GREEN}============================================================${NC}"

# Check dependencies
echo -e "\n${YELLOW}[1/6] Checking dependencies...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: python3 is required${NC}"
    exit 1
fi

if ! python3 -c "from fontTools import ttLib" &> /dev/null; then
    echo -e "${YELLOW}Installing fonttools...${NC}"
    pip3 install fonttools
fi
echo -e "${GREEN}✓ Dependencies OK${NC}"

# Download Hack font
echo -e "\n${YELLOW}[2/6] Downloading Hack font...${NC}"
if [ ! -d "hack_font" ]; then
    curl -L -o Hack-v3.003-ttf.zip https://github.com/source-foundry/Hack/releases/download/v3.003/Hack-v3.003-ttf.zip
    unzip -o Hack-v3.003-ttf.zip -d hack_font
    rm Hack-v3.003-ttf.zip
    echo -e "${GREEN}✓ Hack font downloaded${NC}"
else
    echo -e "${GREEN}✓ Hack font already exists${NC}"
fi

# Download LINE Seed JP font
echo -e "\n${YELLOW}[3/6] Downloading LINE Seed JP font...${NC}"
if [ ! -d "line_seed_font" ]; then
    curl -L -o LINE_Seed_JP.zip "https://seed.line.me/src/images/fonts/LINE_Seed_JP.zip"
    mkdir -p line_seed_font
    unzip -o LINE_Seed_JP.zip -d line_seed_font
    rm LINE_Seed_JP.zip
    echo -e "${GREEN}✓ LINE Seed JP font downloaded${NC}"
else
    echo -e "${GREEN}✓ LINE Seed JP font already exists${NC}"
fi

# Download LINE Seed KR font
echo -e "\n${YELLOW}[4/6] Downloading LINE Seed KR font...${NC}"
if [ ! -d "line_seed_font_kr" ]; then
    curl -L -o LINE_Seed_KR.zip "https://seed.line.me/src/images/fonts/LINE_Seed_Sans_KR.zip"
    mkdir -p line_seed_font_kr
    unzip -o LINE_Seed_KR.zip -d line_seed_font_kr
    rm LINE_Seed_KR.zip
    echo -e "${GREEN}✓ LINE Seed KR font downloaded${NC}"
else
    echo -e "${GREEN}✓ LINE Seed KR font already exists${NC}"
fi

# Build HackLine fonts
echo -e "\n${YELLOW}[5/6] Building HackLine fonts...${NC}"
python3 merge_fonts.py
echo -e "${GREEN}✓ HackLine fonts generated${NC}"

# Build Nerd Font version (optional)
if [ "$1" = "--nerd" ] || [ "$1" = "-n" ]; then
    echo -e "\n${YELLOW}[6/6] Building Nerd Font version...${NC}"
    
    if [ ! -d "HackNerdFont" ]; then
        echo "Downloading HackNerdFont..."
        curl -L -o HackNerdFont.zip https://github.com/ryanoasis/nerd-fonts/releases/download/v3.3.0/Hack.zip
        unzip -o HackNerdFont.zip -d HackNerdFont
        rm HackNerdFont.zip
    fi
    
    python3 add_nerd_glyphs.py
    echo -e "${GREEN}✓ Nerd Font version generated${NC}"
else
    echo -e "\n${YELLOW}[5/5] Skipping Nerd Font version (use --nerd to enable)${NC}"
fi

# Summary
echo -e "\n${GREEN}============================================================${NC}"
echo -e "${GREEN}Build Complete!${NC}"
echo -e "${GREEN}============================================================${NC}"
echo -e "Generated fonts in ${YELLOW}build/${NC}:"
ls -lh build/*.ttf

# Create release zips
echo -e "\n${YELLOW}Creating release zip files...${NC}"
cd build
zip -j HackLine-All.zip HackLine-Regular.ttf HackLine-Bold.ttf HackLineJK-Regular.ttf HackLineJK-Bold.ttf HackLineNF-Regular.ttf HackLineNF-Bold.ttf HackLineJKNF-Regular.ttf HackLineJKNF-Bold.ttf
zip -j HackLineJP.zip HackLine-Regular.ttf HackLine-Bold.ttf HackLineNF-Regular.ttf HackLineNF-Bold.ttf
zip -j HackLineJK.zip HackLineJK-Regular.ttf HackLineJK-Bold.ttf HackLineJKNF-Regular.ttf HackLineJKNF-Bold.ttf
cd ..
echo -e "${GREEN}✓ Release zip files created in build/${NC}"
ls -lh build/*.zip
