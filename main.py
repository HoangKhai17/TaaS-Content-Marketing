"""
main.py — Entry point cho TaaS Content Marketing Skill
"""

import argparse
from utils.ghost_client import GhostClient
from utils.image_generator import ImageGenerator
from utils.seo_validator import SEOValidator


def main():
    parser = argparse.ArgumentParser(description="TaaS Content Marketing Skill")
    parser.add_argument("--topic", required=True, help="Chủ đề bài viết")
    parser.add_argument(
        "--type",
        required=True,
        choices=["tin-cong-ty", "tin-cong-nghe", "case-study", "insight"],
        help="Loại bài viết",
    )
    parser.add_argument("--tag", required=True, help="Tag Ghost CMS")
    args = parser.parse_args()

    print(f"Topic: {args.topic}")
    print(f"Type:  {args.type}")
    print(f"Tag:   {args.tag}")

    # TODO: implement pipeline


if __name__ == "__main__":
    main()
