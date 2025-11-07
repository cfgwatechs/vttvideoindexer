import json
import re
import azure.functions as func

async def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
        vtt_content = req_body.get('vtt_content')
        video_id = req_body.get('video_id')
        video_title = req_body.get('video_title')
        vimeo_url = req_body.get('vimeo_url')

        if not all([vtt_content, video_id, video_title, vimeo_url]):
            return func.HttpResponse(
                "Please pass all required fields in the request body",
                status_code=400
            )

        result = convert_vtt_to_json(vtt_content, video_id, video_title, vimeo_url)
        return func.HttpResponse(result, mimetype="application/json")
        
    except ValueError:
        return func.HttpResponse(
            "Invalid JSON in request body",
            status_code=400
        )

def convert_vtt_to_json(vtt_content: str, video_id: str, video_title: str, vimeo_url: str) -> str:
    """
    Converts WEBVTT content into the specified JSON format.

    Args:
        vtt_content: A string containing the full content of the .vtt file.
        video_id: The Vimeo video ID.
        video_title: The title of the video.
        vimeo_url: The full URL to the Vimeo video.

    Returns:
        A JSON formatted string.
    """
    
    # The main data structure
    output_data = {
        "videoId": video_id,
        "videoTitle": video_title,
        "vimeoUrl": vimeo_url,
        "transcript": []
    }

    # Split the VTT file into individual cue blocks. Cues are separated by double newlines.
    # We filter out any empty strings that might result from the split.
    cue_blocks = [block for block in vtt_content.strip().split('\n\n') if block]

    # The first block is often just "WEBVTT", so we skip it if that's the case.
    if cue_blocks and "WEBVTT" in cue_blocks[0]:
        cue_blocks.pop(0)

    for block in cue_blocks:
        lines = block.split('\n')
        
        # Skip any malformed blocks that don't have at least a timestamp and text
        if len(lines) < 2:
            continue

        # The timestamp line is usually the first or second line (if there's a cue number)
        # We find it by looking for the '-->' separator.
        timestamp_line = ""
        text_lines = []
        
        found_timestamp = False
        for line in lines:
            if '-->' in line:
                timestamp_line = line
                found_timestamp = True
            elif found_timestamp:
                # All subsequent lines are part of the text
                text_lines.append(line)

        if not timestamp_line:
            continue
            
        try:
            # Extract start and end times. We are only interested in HH:MM:SS.
            start_time_full, end_time_full = timestamp_line.split(' --> ')
            start_time = start_time_full.split('.')[0]
            end_time = end_time_full.split('.')[0]

            # Join the text lines together, stripping any leading/trailing whitespace
            text = " ".join(line.strip() for line in text_lines).strip()
            
            if text: # Only add entries that have text
                output_data["transcript"].append({
                    "startTime": start_time,
                    "endTime": end_time,
                    "text": text
                })
        except ValueError:
            # This handles cases where the timestamp line is malformed.
            print(f"Skipping malformed block: {block}")
            continue

    # Convert the Python dictionary to a JSON string
    return json.dumps(output_data, indent=2)