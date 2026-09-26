# gcp-serverless-image-pipeline

## 1. Project Overview
This document outlines the deployment of an event-driven, serverless image processing pipeline using GCP Cloud Run Functions. The system automatically intercepts image upload events, normalizes color spaces, resizes dimensions while maintaining aspect ratio, and applies lossless/lossy compression before storing the output in a target Cloud Storage bucket.

---

## 2. Architecture Diagram
![Architecture Diagram](./architecture-diagram.png)

---

## 3. Step 1: Cloud Storage Buckets Creation
### a. Create Cloud Storage Buckets
1. Navigate to the Google Cloud Console.
2. Create a new bucket to act as the source bucket (e.g., `source-bucket-xyz`).
3. Create a second bucket to act as the destination bucket (e.g., `destination-bucket-xyz`).

---

## 4. Step 2: Pub/Sub Topic and Event Notification Setup
### a. Create a Pub/Sub Topic:
1. Open Cloud Shell and execute:
   ```bash
   TOPIC=add_image
   gcloud pubsub topics create $TOPIC
   
