# Issue Explanation: Incorrect OpenAI API Image Format

## What Happened?

The application contains a bug in the `interpret_image_to_text()` function in `app.py` (lines 96-131) that prevents image uploads from working correctly with the OpenAI API.

## The Problem

### Incorrect Code (Lines 114-121)
```python
{
    "role": "user",
    "content": [
        {
            "type": "input_image",  # ❌ WRONG: Should be "image_url"
            "image": {              # ❌ WRONG: Should be "image_url"
                "data": b64,        # ❌ WRONG: Should be in "url" field
                "media_type": mime_type,  # ❌ WRONG: Should be part of data URL
            },
        },
        # ... rest of content
    ],
}
```

### Issues Identified

1. **Incorrect Type**: Uses `"input_image"` instead of the correct `"image_url"`
2. **Wrong Structure**: Uses `"image": {"data": ..., "media_type": ...}` instead of `"image_url": {"url": ...}`
3. **Incorrect Data Format**: The base64 data and media type should be combined into a data URL format

### Impact

This bug would cause the following symptoms:
- Image upload feature fails completely
- Users cannot get narrations for uploaded images (PNG, JPG, JPEG, GIF, WEBP)
- API would return errors when trying to process images
- The vision adapter functionality advertised in the README would not work

## The Fix

### Correct Code Format
```python
{
    "role": "user",
    "content": [
        {
            "type": "image_url",  # ✅ CORRECT
            "image_url": {        # ✅ CORRECT
                "url": f"data:{mime_type};base64,{b64}"  # ✅ CORRECT
            },
        },
        {
            "type": "text",
            "text": "Describe this image for spoken narration.",
        },
    ],
}
```

## Why This Matters

According to the OpenAI API documentation:
- Vision-enabled models (like `gpt-4o-mini` used in this app) require images in the `image_url` format
- The image data must be provided as a data URL: `data:image/{mimetype};base64,{base64_data}`
- Supported formats: PNG, JPEG, WEBP, and non-animated GIF
- Up to 10 images can be included per chat request

## Status: Fixed ✅

The bug has been corrected in this PR. The `interpret_image_to_text()` function now uses the proper OpenAI API format for image inputs.

## Testing Recommendations

After merging this fix, test the following scenarios:
1. Upload a PNG image and verify it generates narration
2. Upload a JPEG image and verify it works
3. Upload an image with text content and verify the vision model can read it
4. Upload a chart/graph and verify the trend description works
5. Test with various image sizes to ensure proper handling

## Related Files

- `app.py` - Lines 96-131 (the `interpret_image_to_text()` function)
- `README.md` - Documents the image upload feature

## References

- [OpenAI Vision API Documentation](https://platform.openai.com/docs/guides/images-vision)
- [GPT-4o Vision Examples](https://community.openai.com/t/supported-attachments-formats/966387)
