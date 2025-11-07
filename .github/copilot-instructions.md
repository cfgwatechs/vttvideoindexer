# VTT Video Indexer AI Agent Instructions

## Project Overview
This is a Python Azure Function that converts WebVTT subtitle files to a structured JSON format and stores them in Azure Blob Storage. The project serves as a video transcript indexing service.

## Key Components & Architecture

### Core Processing (`__init__.py`)
- Main conversion logic in `convert_vtt_to_json()` function
- Takes VTT content and video metadata (id, title, URL) as input
- Outputs standardized JSON format with video metadata and timestamped transcript entries

### Output JSON Structure
```json
{
  "videoId": "string",
  "videoTitle": "string",
  "vimeoUrl": "string",
  "transcript": [
    {
      "startTime": "HH:MM:SS",
      "endTime": "HH:MM:SS",
      "text": "string"
    }
  ]
}
```

## Development Setup
1. Install Azure Functions Core Tools:
   ```bash
   # On macOS with Homebrew
   brew tap azure/functions
   brew install azure-functions-core-tools@4

   # Verify installation
   func --version
   ```

2. Configure local Azure Function development environment:
   - Set Azure Storage connection string in `local.settings.json`
   - Install Python 3.9+ (required for Azure Functions)

3. Required Python dependencies (`requirements.txt`):
   ```
   azure-functions
   azure-storage-blob
   ```

## Azure Integration
- Uses Azure Functions Python runtime
- Requires Azure Blob Storage for output
- Key configuration in `local.settings.json`:
  - `AzureWebJobsStorage`: Storage account for Functions
  - `AzureBlobStorageConnectionString`: Target blob storage for transcripts

## Project Conventions
- Time format: HH:MM:SS (milliseconds stripped from timestamps)
- Transcript entries skipped if text is empty
- VTT block validation:
  - Must have timestamp line with "-->" separator
  - Must have non-empty text content
  - Malformed blocks logged and skipped gracefully

## Deployment Guide

### Local Development
1. Start local Azure Storage Emulator:
   ```bash
   azurite --silent --location /path/to/azurite
   ```

2. Run function locally:
   ```bash
   func start
   ```

### Production Deployment
1. Create required Azure resources:
   ```bash
   az group create --name vttvideoindexer-rg --location eastus
   az storage account create --name vttindexerstorage --resource-group vttvideoindexer-rg
   az functionapp create --name vttvideoindexer --storage-account vttindexerstorage --runtime python --runtime-version 3.9 --functions-version 4 --resource-group vttvideoindexer-rg --consumption-plan-location eastus
   ```

2. Configure app settings:
   ```bash
   az functionapp config appsettings set --name vttvideoindexer --resource-group vttvideoindexer-rg --settings "AzureBlobStorageConnectionString=your_connection_string"
   ```

3. Deploy using Azure Functions Core Tools:
   ```bash
   func azure functionapp publish vttvideoindexer
   ```

### Post-Deployment Verification
1. Check function logs:
   ```bash
   az functionapp logs tail --name vttvideoindexer --resource-group vttvideoindexer-rg
   ```

2. Test endpoint with sample VTT file:
   ```bash
   curl -X POST https://vttvideoindexer.azurewebsites.net/api/convert \
     -H "Content-Type: application/json" \
     -d '{"vtt_content": "...", "video_id": "123", "video_title": "Test", "vimeo_url": "https://vimeo.com/123"}'
   ```

## Common Issues & Debugging
- Missing storage connection strings in `local.settings.json`
- Malformed VTT blocks handled via try-except blocks with logging
- Invalid timestamp formats skipped with debug output
- Deployment failures often related to Python version mismatch - ensure local Python version matches Azure Functions runtime version
- Scale issues may require adjusting host.json configuration for batch size and concurrency

For detailed Azure Functions debugging guidance, refer to [Azure Functions Python developer guide](https://docs.microsoft.com/azure/azure-functions/functions-reference-python).