from typing import List, Tuple, Dict

from notion_exporter import NotionExporter as _NotionExporter
import frontmatter
from haystack import component  
from haystack.dataclasses import Document

from ._custom_yaml_handler import CustomYAMLHandler

@component
class NotionExporter():

    def __init__(
        self,
        api_token: str,
        export_child_pages: bool = False,
        extract_page_metadata: bool = False,
        exclude_title_containing: str = None,
    ):
        """
        Initialize the NotionExporter component. This component is used to export pages from Notion and convert them
        to Haystack Documents.

        :param api_token: The Notion API token.
        :param export_child_pages: Whether to recursively export all child pages of the provided page ids.
            Defaults to False.
        :param extract_page_metadata: Whether to extract metadata from the page and add it as a frontmatter to the
            markdown. Extracted metadata includes title, author, path, URL, last editor, and last editing time
            of the page. Defaults to False.
        :param exclude_title_containing: If specified, pages with titles containing this string will be excluded.
            This might be useful for example to exclude pages that are archived. Defaults to None.
        """
        self.notion_exporter = _NotionExporter(
            notion_token=api_token,
            export_child_pages=export_child_pages,
            extract_page_metadata=extract_page_metadata,
            exclude_title_containing=exclude_title_containing,
        )

    @component.output_types(documents=List[Document])
    def run(self, page_ids: List[str]):
        """
        Export Notion pages to Haystack Documents by providing a list of Notion page IDs.

        :param page_ids: A list of Notion page IDs to export.
        """
        extracted_pages = self.notion_exporter.export_pages(page_ids)

        custom_yaml_handler = CustomYAMLHandler()
        documents = []
        for page_id, page in extracted_pages.items():
            metadata, markdown_text = frontmatter.parse(page, handler=custom_yaml_handler)
            document = Document(meta=metadata, content=markdown_text)
            documents.append(document)

        return {"documents": documents}






