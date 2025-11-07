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