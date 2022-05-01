"""
Configuration for report generation.
"""

# The endpoint for report generation
# TODO(Kyle): We need a way to manage this endpoint,
# specifically the ability to change it without the
# need to re-publish the entire mlte source package.
REPORT_GENERATION_ENDPOINT = (
    "https://p4u27iv9qf.us-east-1.awsapprunner.com/html"
)
