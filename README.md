# PIA MCP Examples

This directory contains example scripts demonstrating how to integrate the PIA MCP Server with LangChain and various LLM providers.

## LangChain MCP Integration Example

This example shows how to connect to the PIA MCP Server, discover available tools, and use them with AI agents powered by OpenAI, Azure OpenAI, or Claude models.

### Features

- **Remote MCP Connection**: Connect to the PIA MCP server via HTTP/SSE using official `langchain-mcp-adapters`
- **Dynamic Tool Discovery**: Automatically discover and load all available MCP tools
- **Multiple LLM Support**: Works with OpenAI, Azure OpenAI, and Claude (Anthropic) models
- **LangChain Integration**: Seamlessly integrate MCP tools with LangChain agents using modern LangChain 1.0 API
- **Example Queries**: Includes working examples for common use cases

### Files in This Directory

- `langchain_mcp_example.py` - Complete working example script
- `requirements.txt` - Python dependencies for the example
- `env.example` - Environment variable template (copy to `.env`)
- `README.md` - This file

**Implementation Note**: This example uses the official `langchain-mcp-adapters` package to connect to remote HTTP/SSE MCP servers. The implementation uses:
- `MultiServerMCPClient` with `streamable_http` transport for remote MCP servers
- `create_agent` from LangChain 1.0 for modern agent creation
- Automatic tool discovery and conversion to LangChain tools
- Works with any tool-calling LLM (OpenAI, Azure, Claude)

## Quick Start

### 1. Set Up Virtual Environment (Recommended)

Using a virtual environment keeps dependencies isolated:

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Your prompt should now show (venv) indicating the venv is active
```

### 2. Install Dependencies

```bash
# Make sure your virtual environment is activated
pip install -r requirements.txt
```

### 3. Configure Environment Variables

```bash
# Copy the example environment file
cp env.example .env

# Edit .env with your actual API keys
# Use your preferred text editor:
nano .env
# or
vim .env
# or
code .env  # VS Code
```

**Required variables:**
- `PIA_API_KEY` - Get from [https://mcp.programintegrity.org/get-api-key](https://mcp.programintegrity.org/get-api-key). If you don't have a PIA Community account, follow the links to create one
- `LLM_PROVIDER` - Choose: `openai`, `azure`, or `claude`
- Provider-specific API keys (see env.example for details)

You only need to configure one LLM provider, but feel free to set up multiple for comparison.

### 4. Run the Example

```bash
# Make sure your virtual environment is activated
# Run with default example queries:
python langchain_mcp_example.py

# Or run with your own query:
python langchain_mcp_example.py "What is ambulance fraud?"

# Another example:
python langchain_mcp_example.py "Find recent cybersecurity reports from OIGs"
```

```

## LLM Provider Setup

Choose one of the following providers and configure the corresponding environment variables in your `.env` file:

### OpenAI (Default)

```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...your-openai-api-key...
OPENAI_MODEL=gpt-4  # optional, default: gpt-4
```

**Get API Key:** https://platform.openai.com/api-keys

### Azure OpenAI

```bash
LLM_PROVIDER=azure
AZURE_OPENAI_API_KEY=your-azure-api-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=your-deployment-name
AZURE_OPENAI_API_VERSION=2024-02-15-preview  # optional
```

**Setup Requirements:**
1. Azure subscription
2. Azure OpenAI resource created in Azure Portal
3. Model deployment (GPT-5, GPT-5-mini, etc.)
4. Get credentials from: https://portal.azure.com

### Claude (Anthropic)

```bash
LLM_PROVIDER=claude
ANTHROPIC_API_KEY=sk-ant-...your-anthropic-api-key...
CLAUDE_MODEL=claude-3-5-sonnet-20241022  # optional
```

**Get API Key:** https://console.anthropic.com/

### Hugging Face

```bash
LLM_PROVIDER=huggingface
HUGGINGFACE_API_KEY=hf_...your-huggingface-token...
HUGGINGFACE_MODEL=meta-llama/Llama-3.3-70B-Instruct  # optional
```

**Get API Key:** https://huggingface.co/settings/tokens

## What the Example Does

1. **Connects to PIA MCP Server** - Establishes HTTP connection to https://mcp.programintegrity.org
2. **Initializes MCP Session** - Performs MCP protocol handshake
3. **Discovers Tools** - Retrieves all available search tools (GAO, OIG, CRS, DOJ, Congress.gov, Executive Orders)
4. **Converts to LangChain Tools** - Wraps each MCP tool as a LangChain `StructuredTool`
5. **Creates AI Agent** - Sets up a LangChain agent with your chosen LLM
6. **Executes Queries** - Agent automatically selects and calls appropriate tools to answer questions

## Available MCP Tools

The script automatically discovers these tools from the PIA MCP server:

**General Search Tools:**
- `pia_search_content` - Search document content and recommendations
- `pia_search_content_facets` - Get available filter values
- `pia_search_titles` - Search document titles only

**Data Source-Specific Tools:**
- `pia_search_content_gao` - GAO reports and recommendations
- `pia_search_content_oig` - Oversight.gov (Inspector General reports)
- `pia_search_content_crs` - Congressional Research Service reports
- `pia_search_content_doj` - Department of Justice documents
- `pia_search_content_congress` - Congress.gov legislation
- `pia_search_content_executive_orders` - Federal Register executive orders

**Utility Tools:**
- `referenced_agencies` - Get list of agencies in database

## Example Queries

```bash
# Search for fraud-related recommendations
python langchain_mcp_example.py "Find open recommendations about fraud from GAO"

# Search executive orders
python langchain_mcp_example.py "What executive orders address artificial intelligence?"

# Search recent reports
python langchain_mcp_example.py "Show me the latest cybersecurity reports from OIG"

# Search across multiple sources
python langchain_mcp_example.py "Find recommendations about improper payments"

# Get specific information
python langchain_mcp_example.py "What agencies are most mentioned in DOJ documents?"
```

## Troubleshooting

### Virtual Environment Issues

**Problem:** `python3: command not found`
```bash
# Try using 'python' instead of 'python3':
python -m venv venv
```

**Problem:** Virtual environment not activating
```bash
# Make sure you're in the examples directory
pwd  # Should show: .../pia-mcp/examples

# Try activating again:
source venv/bin/activate

# Check if it worked (you should see (venv) in your prompt):
which python  # Should show: .../examples/venv/bin/python
```

### Dependency Installation Issues

**Problem:** `pip: command not found`
```bash
# Make sure your virtual environment is activated
# Then try:
python -m pip install -r requirements.txt
```

**Problem:** Permission denied errors
```bash
# This shouldn't happen with venv, but if it does:
# Make sure your virtual environment is activated (you should see (venv) in prompt)
# If still having issues, recreate the venv:
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### API Key Errors

**Problem:** `PIA_API_KEY environment variable is required`
```bash
# Make sure you created and edited the .env file:
ls -la .env  # File should exist
cat .env     # Should show your configuration

# Make sure you're running from the examples directory:
pwd  # Should show: .../pia-mcp/examples
```

**Problem:** `OPENAI_API_KEY environment variable is required`
- Verify you set the correct API key for your chosen `LLM_PROVIDER` in `.env`
- For Azure, you need `AZURE_OPENAI_API_KEY`, not `OPENAI_API_KEY`
- For Claude, you need `ANTHROPIC_API_KEY`

### Connection Issues

**Problem:** `Connection timeout` or `Connection refused`
```bash
# Check your internet connection
curl https://mcp.programintegrity.org/health

# Verify the PIA_MCP_URL in your .env file:
cat .env | grep PIA_MCP_URL
# Should show: PIA_MCP_URL=https://mcp.programintegrity.org
```

### Import Errors

**Problem:** `ModuleNotFoundError: No module named 'langchain'`
```bash
# Make sure your virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep langchain
```

## Advanced Usage

### Using Different Models

Edit your `.env` file to use different models:

```bash
# OpenAI - use GPT-4 Turbo
OPENAI_MODEL=gpt-4-turbo

# Claude - use Claude Opus
CLAUDE_MODEL=claude-3-opus-20240229

# Hugging Face - use Mistral
HUGGINGFACE_MODEL=mistralai/Mistral-7B-Instruct-v0.2
```

### Switching Between Providers

You can quickly switch providers by changing one line in `.env`:

```bash
# To use OpenAI:
LLM_PROVIDER=openai

# To use Azure:
LLM_PROVIDER=azure

# To use Claude:
LLM_PROVIDER=claude
```

Then run the script again - no code changes needed!

### Customizing the Agent

Edit `langchain_mcp_example.py` to customize:
- Agent system prompt (line ~342)
- Temperature and other LLM parameters (lines ~253-306)
- Tool selection and filtering (lines ~233-238)

## Getting API Keys

### PIA MCP Server (Required)
Register at: https://mcp.programintegrity.org/register

### LLM Providers (Choose One)
- **OpenAI**: https://platform.openai.com/api-keys
- **Azure OpenAI**: https://portal.azure.com (requires Azure subscription)
- **Claude/Anthropic**: https://console.anthropic.com/
- **Hugging Face**: https://huggingface.co/settings/tokens

## Complete Setup Example (Step-by-Step)

Here's a complete walkthrough from scratch:

```bash
# 1. Navigate to examples directory
cd /path/to/pia-mcp/examples

# 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # You should see (venv) in your prompt

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy environment template
cp env.example .env

# 5. Edit .env file (use your preferred editor)
nano .env
# Add your PIA_API_KEY
# Choose your LLM_PROVIDER
# Add the corresponding API key

# 6. Save and close the editor (Ctrl+X, then Y, then Enter for nano)

# 7. Test the setup
python langchain_mcp_example.py "Test query: find fraud reports"

# 8. When done, deactivate virtual environment
deactivate
```

## Support

- **Main Documentation**: See [../README.md](../README.md) for PIA MCP Server documentation
- **Issues**: Open an issue on the GitHub repository
- **Questions**: Check the troubleshooting section above

## Contributing

Have improvements or additional examples? Contributions are welcome!

1. Create your example script
2. Add comprehensive documentation
3. Include a `requirements.txt` if needed
4. Update this README
5. Submit a pull request

