import pandas as pd
import os

# ---------------- LOAD DATA ----------------
df = pd.read_csv("support_tickets/support_tickets.csv")

docs = []
doc_sources = []

for root, dirs, files in os.walk("data"):
    for file in files:
        if file.endswith(".txt") or file.endswith(".md"):
            file_path = os.path.join(root, file)

            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().lower()
                docs.append(content)
                doc_sources.append(root.lower())

# ---------------- LOG FUNCTION ----------------
def log_message(message):
    log_dir = os.path.expanduser("~\\hackerrank_orchestrate")
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, "log.txt")

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(message + "\n")


# ---------------- CLASSIFICATION ----------------
def classify_request_type(text):
    if any(x in text for x in ["down", "not working", "error", "failed"]):
        return "bug"
    elif any(x in text for x in ["thank", "thanks", "hello", "hi"]):
        return "invalid"
    else:
        return "product_issue"


def classify_product_area(text):
    if any(x in text for x in ["test", "interview", "submission", "assessment"]):
        return "screen"
    elif any(x in text for x in ["login", "signup", "register", "community", "account"]):
        return "community"
    elif any(x in text for x in ["conversation", "chat"]):
        return "conversation_management"
    elif any(x in text for x in ["privacy", "data"]):
        return "privacy"
    elif any(x in text for x in ["visa", "card"]):
        if any(x in text for x in ["travel", "stolen"]):
            return "travel_support"
        else:
            return "general_support"
    else:
        return "screen"


def classify_status(request_type):
    return "Escalated" if request_type == "bug" else "Replied"


# ---------------- JUSTIFICATION ----------------
def generate_justification(text, request_type):
    keywords = ["down", "error", "failed", "not working"]
    found = [k for k in keywords if k in text]

    if request_type == "bug":
        return f"Detected issue using keywords: {', '.join(found)} → escalated"
    elif request_type == "invalid":
        return "Non-actionable query"
    else:
        return "Mapped to support category using documentation"


# ---------------- RESPONSE ----------------
def generate_response(text, company):
    stopwords = {"the","is","in","to","and","of","for","on","a","an","my","i","we","you"}

    words = [w for w in text.split() if w not in stopwords]
    important_words = [w for w in words if len(w) > 4]

    best_sentence = ""
    max_score = 0

    for doc, source in zip(docs, doc_sources):

        if company.lower() not in source:
            continue

        sentences = doc.split("\n")

        for sentence in sentences:
            sentence = sentence.strip()

            if (
                len(sentence) < 20 or
                sentence.startswith("#") or
                "source_url" in sentence or
                "http" in sentence
            ):
                continue

            sentence = sentence.replace("#", "").replace("*", "")

            if important_words:
                match_count = sum(1 for w in important_words if w in sentence)
                if match_count < 2:
                    continue

            score = sum(2 for w in important_words if w in sentence) + \
                    sum(1 for w in words if w in sentence)

            if score > max_score:
                max_score = score
                best_sentence = sentence

    if best_sentence:
        best_sentence = best_sentence.strip()

        if best_sentence.endswith("?"):
            return "Please refer to official documentation."

        return best_sentence

    return "Please refer to official documentation."


# ---------------- MAIN LOOP ----------------
output = []

for index, row in df.iterrows():
    issue = str(row["Issue"]).replace("\n", " ").strip()
    subject = str(row["Subject"]).replace("\n", " ").strip()
    company = str(row["Company"]).replace("\n", " ").strip()

    text = (issue + " " + subject + " " + company).lower()

    request_type = classify_request_type(text)
    product_area = classify_product_area(text)
    status = classify_status(request_type)
    justification = generate_justification(text, request_type)
    response = generate_response(text, company)

    # -------- LOGGING --------
    log_message(f"""
[START]

Issue: {issue}
Subject: {subject}
Company: {company}

Request Type: {request_type}
Product Area: {product_area}
Status: {status}

Justification: {justification}
Response: {response}

--------------------------------------------------
""")

    output.append({
        "Issue": issue,
        "Subject": subject,
        "Company": company,
        "Response": response,
        "Product Area": product_area,
        "Status": status,
        "Request Type": request_type,
        "Justification": justification
    })

# ---------------- SAVE ----------------
out_df = pd.DataFrame(output)
out_df.to_csv("support_tickets/output.csv", index=False, encoding="utf-8-sig")

print("Done ✅ Output saved")
print("Log file created at: C:\\Users\\<your-user>\\hackerrank_orchestrate\\log.txt")