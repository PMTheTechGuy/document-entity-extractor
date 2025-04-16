from extractor.text_extractor import extract_info

sample_text = """
John Smith is a senior engineer at Microsoft. You can contact him at john.smith@microsoft.com.
"""

names, emails, orgs = extract_info(sample_text)

print("Names:", names)
print("Emails:", emails)
print("Organizations:", orgs)
