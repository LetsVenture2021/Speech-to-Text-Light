# Speech-to-Text Light

Speech-to-Text Light is a streamlined listening companion that transforms any incoming content into adaptive speech. It ingests links, files, pasted text, visuals, and real-time voice prompts, then routes each input through an emotion-aware processing loop to produce contextually aligned narration.

## Features

- **Link ingestion**: Accept URLs dropped into the chat box, fetch remote content, and send it through the semantic layer pipeline (Emotion Inference ➝ Identity Kernel) so the spoken response mirrors the source tone before replying.
- **Direct paste reading**: Route pasted passages through the Inflective Emergence Loop to deliver emotionally aligned narration while maintaining drift-aware memory for continuity.
- **Document uploads**: Parse PDF, Word, or plain-text uploads, interpret section by section, and feed the results into the loop so persona responses evolve with the document context.
- **Image uploads**: Use a vision adapter to derive descriptive cues, then hand them to the prosody engine for expressive narration while drift tracking updates conversational history.
- **Data file uploads**: Summarize structured inputs (e.g., XLSX, SQL extracts) with specialized interpreters before passing highlights into the Inflection stage for balanced spoken insights.
- **Theory context shaping**: Apply stored theoretical frames to explain findings in voices that match the target explanatory tone.
- **Data visuals**: Parse graphs and diagrams to identify trends, translate them into narrative intent, and produce engaging spoken walkthroughs.
- **Real-time speech**: Transcribe live user audio, process it through the loop, and answer with adaptive prosody that respects ongoing identity drift.

## Purpose

The application focuses on rapid, natural listening. Users can hand it any form of content and receive an immediate audio response that:

1. Removes the friction of reading long-form material manually.
2. Preserves the emotional and contextual cues embedded in the source.
3. Maintains a coherent persona that adapts gently with each interaction.
4. Keeps the experience lightweight so the user can stay hands-free and focused.

## UI and Layout

1. Primary input field for typing or pasting content.
2. Paperclip button on the left edge of the input for quick document uploads.
3. Speech icon button on the right edge to initiate voice prompting.
4. Upload/send icon next to the speech button for submitting typed or pasted prompts.
5. App replies exclusively in speech after processing any submitted prompt.
6. For spoken prompts, the app auto-sends once it detects three seconds of silence.

## Interaction Flow

1. User submits content (typed, pasted, uploaded, or spoken).
2. Input travels through the semantic layer and Inflective Emergence Loop to infer emotion, identity drift, and explanatory goals.
3. Processed content routes to the prosody engine to shape delivery.
4. The app replies with speech, updating the drift-aware memory for future turns.

## Getting Started (Conceptual)

- Provide a URL, paste text, or upload files/images/data via the input field controls.
- Alternatively, press the speech icon and speak; the app auto-sends after silence is detected.
- Listen to the generated narration and continue interacting hands-free.

## Roadmap Ideas

- Inline visualization of processing stages for debugging or transparency.
- User-tunable personas and tone presets.
- Exportable summaries alongside audio responses.
- Mobile-friendly layout with voice-first shortcuts.

## Contributing

Interested in contributing to this project? We welcome contributions!

If you're new to Git or need help understanding how to work with branches, commits, pulls, and merges, check out our comprehensive [Contributing Guide](CONTRIBUTING.md). It includes:

- Git basics and concepts explained clearly
- How to navigate between branches
- Step-by-step workflows for making changes
- Understanding commits, pulls, and merges
- Common troubleshooting tips
- Pull request best practices

Even if you're experienced with Git, the guide contains project-specific workflows and conventions that will help you contribute effectively.
