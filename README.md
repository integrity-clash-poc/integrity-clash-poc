# Integrity Clash: A2A Protocol Vulnerability Proof of Concept

This repository contains the software artifact and Proof of Concept (PoC) demonstrating the "Integrity Clash" vulnerability within Agent-to-Agent (A2A) protocols.

## Overview

Emerging A2A protocols are vulnerable to systemic orchestration flaws. While existing research primarily addresses static threats, this repository introduces a novel dynamic attack known as the Integrity Clash. This vulnerability manifests when a message is perfectly authenticated by the protocol but fundamentally breaks the logic window of the receiving Large Language Model (LLM). By combining a semantic flaw (a hidden malicious payload) with a cryptographic network flaw (unauthenticated Server-Sent Events, or SSE), an attacker can force the host agent into a "confused deputy" state. Using an open-weight LLM, this artifact demonstrates how state-machine asynchrony causes task desynchronization, ultimately leading to the unauthorized execution of restricted actions.

## Prerequisites & Installation

* **Hardware Requirements:** Execution requires a GPU with sufficient VRAM to load the Qwen/Qwen2.5-7B-Instruct model. The scripts are configured to load this model into GPU memory using the bfloat16 data type and automatic device mapping.
* **Software Requirements:** The environment must have torch, transformers, and accelerate installed.

Execute the following command to install the required dependencies:

`pip install torch transformers accelerate`

## Repository Structure

* **travel_poc.py:** This script evaluates the vulnerability within a simulated travel ecosystem utilizing an autonomous travel and booking agent. It demonstrates how a spoofed "BOOKING_CONFIRMED" event injected into an SSE stream tricks the confused deputy into executing a conditional malicious payload that exfiltrates corporate billing data.
* **finance_poc.py:** This script evaluates an enterprise financial agent tasked with executing virements. It demonstrates the exploit bypassing a simulated manual manager review by injecting a spoofed "COMPLETED" SSE event, tricking the LLM into executing an unauthorized fund transfer to an attacker's account.
* **asr_evaluation.py:** This script conducts an automated Attack Success Rate (ASR) evaluation over 50 iterations to statistically validate the exploit's reliability. It tests a baseline static payload injection against the dynamic Integrity Clash exploit.

## Usage Instructions

To run the Travel Scenario PoC:

`python travel_poc.py`

To run the Finance Scenario PoC:

`python finance_poc.py`

To run the automated Attack Success Rate Evaluation:

`python asr_evaluation.py`

## Expected Output

When running travel_poc.py and finance_poc.py, reviewers will observe terminal logs outputting three distinct sequential scenarios:

* **Scenario 1:** A simple safe task is processed and executed immediately without opening an SSE listening stream.
* **Scenario 2 (Baseline):** A high-risk task is halted for approval, resulting in a [DEFENSE UPHELD] log when the legitimate sub-agent or manager rejects the action and the agent aborts.
* **Scenario 3 (Exploit):** The Integrity Clash exploit is simulated by injecting a spoofed asynchronous event. The terminal will log [CRITICAL EXPLOIT SUCCESS] as the Confused Deputy bypasses constraints and executes the unauthorized payload.

When executing asr_evaluation.py, the terminal will display the real-time processing of 50 iterations per scenario. Upon completion, the logs will confirm a 0% Attack Success Rate (0/50 successful attacks) for the baseline static payload injection, contrasted against a 100% Attack Success Rate (50/50 successful attacks) for the Integrity Clash exploit utilizing spoofed SSE.
