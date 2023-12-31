# Lambda Transcript Processor v1.2

The Lambda Transcript Processor is a AWS serverless application designed to seamlessly integrate YouTube video transcripts with the powerful language understanding capabilities of OpenAI's GPT models. This project allows users to start interactive sessions where they can query the transcript content in natural language, receiving contextually relevant responses.

## Features

- **Transcript Initialization**: Start sessions by providing a video transcript to serve as the context for future interactions.
- **Interactive Q&A**: Pose questions about the transcript and receive accurate, context-aware answers generated by GPT-3.5-turbo-1106.
- **Scalable Architecture**: Built on AWS Lambda for on-demand, scalable processing power.
- **Secure API Key Handling**: Uses AWS environment variables to securely manage API keys.
- **DynamoDB Integration**: Leverages Amazon DynamoDB for efficient storage and retrieval of session states.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What you need to install the software:

- AWS CLI
- Python 3.8+
- An AWS account with appropriate permissions

### Installing

A step-by-step series of examples that tell you how to get a development environment running:

1. Clone the repository to your local machine:
```sh
git clone https://github.com/your-username/lambda-transcript-processor-v1.2.git
