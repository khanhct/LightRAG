from __future__ import annotations
from typing import Any


PROMPTS: dict[str, Any] = {}

PROMPTS["DEFAULT_LANGUAGE"] = "English"
PROMPTS["DEFAULT_TUPLE_DELIMITER"] = "<|>"
PROMPTS["DEFAULT_RECORD_DELIMITER"] = "##"
PROMPTS["DEFAULT_COMPLETION_DELIMITER"] = "<|COMPLETE|>"

PROMPTS["DEFAULT_ENTITY_TYPES"] = [
"ProductName", # Main product entity
"ProductID", # Product ID
"Description", # Product Description
"Recommend",# Product Recommendation
"Stock",# Product Stock
"Brand", #Product manufacturer/brand
"Category", #Product category from the specified list
"Sku", #Product SKU code
"Package", #Product package size
"Size", #Product package size short
"Style", #Product styles
"Weight", #Product weight
"Price", #Product price
"Color", #Available color options
"Material", #Materials used in construction
"Feature", #Specific product features (leak guards, tabs, etc.)
"Benefit", #Customer benefits (odor control, comfort, etc.)
"Media", #Product media (video, image, etc.)
"Price", #Product price
"UseCase", #Intended usage scenarios (overnight, daytime, etc.)
"UserType", #Target user demographics (men, women, youth, etc.)
"IncontinenceType", #Type of incontinence addressed
"Specification", #Technical specifications (absorbency, duration, etc.)
"PricePoint", #Pricing category (budget, premium, etc.)
"Competitor", #Referenced competing products
"Accessory", #Related or complementary products
]

PROMPTS["DEFAULT_USER_PROMPT"] = "n/a"

PROMPTS["entity_extraction"] = """---Goal---
Given a text document that is potentially relevant to this activity and a list of entity types, identify all entities of those types from the text and all relationships among the identified entities.
Use {language} as output language.

---Steps---
1. Identify all entities. For each identified entity, extract the following information:
- entity_name: Name of the entity, use same language as input text. If English, capitalized the name.
- entity_type: One of the following types: [{entity_types}]
- entity_description: Comprehensive description of the entity's attributes and activities
Format each entity as ("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_description>)

2. From the entities identified in step 1, identify all pairs of (source_entity, target_entity) that are *clearly related* to each other.
For each pair of related entities, extract the following information:
- source_entity: name of the source entity, as identified in step 1
- target_entity: name of the target entity, as identified in step 1
- relationship_description: explanation as to why you think the source entity and the target entity are related to each other
- relationship_strength: a numeric score indicating strength of the relationship between the source entity and target entity
- relationship_keywords: one or more high-level key words that summarize the overarching nature of the relationship, focusing on concepts or themes rather than specific details
Format each relationship as ("relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_description>{tuple_delimiter}<relationship_keywords>{tuple_delimiter}<relationship_strength>)

Relationship Types:
- IDENTIFIES_PRODUCT: ProductID -> Product  
- DESCRIBES_PRODUCT: ProductID -> ProductName  
- HAS_DESCRIPTION: ProductID -> Description  
- RECOMMENDS_PRODUCT: ProductID -> Recommend  
- HAS_STOCK_LEVEL: ProductID -> Stock  
- BELONGS_TO_BRAND: ProductID -> Brand  
- BELONGS_TO_CATEGORY: ProductID -> Category  
- HAS_PACKAGE: ProductID -> Package  
- HAS_SIZE: ProductID -> Size  
- HAS_STYLE: ProductID -> Style  
- HAS_WEIGHT: ProductID -> Weight  
- PRICED_AT: ProductID -> Price  
- POSITIONED_AS: ProductID -> PricePoint  
- AVAILABLE_IN_COLOR: ProductID -> Color  
- MADE_OF: ProductID -> Material  
- HAS_FEATURE: ProductID -> Feature  
- PROVIDES_BENEFIT: ProductID -> Benefit  
- USED_BY: ProductID -> UserType  
- SUITABLE_FOR: ProductID -> IncontinenceType  
- USED_IN_SCENARIO: ProductID -> UseCase  
- HAS_SPECIFICATION: ProductID -> Specification  
- COMPETES_WITH: ProductID -> Competitor  
- HAS_ACCESSORY: ProductID -> Accessory  
- HAS_MEDIA: ProductID -> Media

3. Identify high-level key words that summarize the main concepts, themes, or topics of the entire text. These should capture the overarching ideas present in the document.
Format the content-level key words as ("content_keywords"{tuple_delimiter}<high_level_keywords>)

4. Return output in {language} as a single list of all the entities and relationships identified in steps 1 and 2. Use **{record_delimiter}** as the list delimiter.

5. When finished, output {completion_delimiter}

######################
---Examples---
######################
{examples}

#############################
---Real Data---
######################
Entity_types: [{entity_types}]
Text:
{input_text}
######################
Output:"""

PROMPTS["entity_extraction_examples"] = [
 """Example 1:

Entity_types: [ProductName, ProductID, Description, ImageLink, Link, Recommend, Stock, Brand, Category, Sku, Package, Size, Style, Weight, Price, Color, Material, Feature, Benefit, Media, UseCase, UserType, IncontinenceType, Specification, PricePoint, Competitor, Accessory]
Text:
```
Product Name: NorthShore EternaDry Diaper Booster Pads (Diaper Doublers)
Product ID: D002-2727
Description: A Booster adds absorbency to a disposable undergarment. When filled with liquid, it flows through into the diaper or brief. NorthShore EternaDry Booster Pads have higher absorbency, more sizes & lower cost than most other brands. Slim, soft & super-absorbent. Has adhesive backing that holds it in place and enables you to stack multiple boosters.
Image Link: https://www.northshorecare.com/globalassets/product-assets/northshore/d002-booster-pads/png/eternadry-pack-no-size.png?width=100
Product Link: https://www.northshorecare.com/incontinence-products/diaper-booster-pads/northshore-booster-pads-contoured-diaper-doublers
Recommend: Y
Stock: 100000
Brand: Crinklz
Category: 
  - Shop For > Incontinence Products for Men > Booster Pads / Doublers
  - Featured Products
  - Shop For > Incontinence Products for Women > Booster Pads / Doublers
  - Brands
  - Adult Diapers > Adult Diaper Booster Pads
  - NorthShore > Booster Pads / Doublers
  - Full NorthShore Catalog
  - Incontinence Products for the Active Golfer
  - Incontinence Products > Booster Pads / Doublers
  - Trial Packs
SKU: 2727
Package: Case/60 (4/15s) - Best Value!
Size: M
Style: Original
Weight: 29.7
Price:
  - Currency Symbol: $
  - List Price: 134.99
  - Sale Price: null
Color: null
Material: Backsheet: Smooth Plastic
Feature: 
  - Leak Guards: Yes
  - Elastic Waistband: Front & Rear
  - Refastenable Tabs: Adhesive
  - Odor Control: Excellent
  - Absorbency: Maximum
  - Absorbent Zone: 13 x 15 x 7 in. Full 26 in.
Benefit: Excellent; Maximum
Use Case: Overnight
User Type: Women, Men, Youth
Incontinence Type: Urinary, Bowel, Urinary+Bowel
Specification: 
  - Absorbency Sort Integer: 30 oz.
  - Fits Weight: 29 - 43 in.
  - Hip Size: 29 - 43 in.
  - Waist Size: 29 - 43 in.
  - Fits Waists: 29 to 36 in., 37 to 48 in.
  - Fits Hips: 29 to 36 in., 37 to 48 in.
  - Product Size: Medium, 29 - 43 in.
  - Model Number: 60500
Price Point: Premium
Competitor: 
Accessory: 
Media:
  - Main Image: /globalassets/product-assets/crinklz/d143-crinklz-briefs/png/crinklz-original-front-package.png
  - Product Assets:
      - Type: Image
        Image URL: /globalassets/product-assets/crinklz/d143-crinklz-briefs/2025/crinklz-original-front-product.jpg
        Alt Text: Crinklz Original Briefs, Brief, Front
      - Type: Image
        Image URL: /globalassets/product-assets/crinklz/d143-crinklz-briefs/2025/crinklz-original-back-product.jpg
        Alt Text: Crinklz Original Briefs, Brief, Rear
  - Images:
      - Type: Image
        Image URL: /globalassets/product-assets/crinklz/d143-crinklz-briefs/2025/crinklz-original-front-product.jpg
        Alt Text: Crinklz Original Briefs, Brief, Front
      - Type: Image
        Image URL: /globalassets/product-assets/crinklz/d143-crinklz-briefs/2025/crinklz-original-back-product.jpg
        Alt Text: Crinklz Original Briefs, Brief, Rear
  - Videos: []
```
Output:
("entity"{tuple_delimiter}"NorthShore EternaDry Diaper Booster Pads (Diaper Doublers)"{tuple_delimiter}"ProductName"{tuple_delimiter}"The full product name describing a booster pad designed for use with diapers to increase absorbency."){record_delimiter}
("entity"{tuple_delimiter}"D002-2727"{tuple_delimiter}"ProductID"{tuple_delimiter}"Unique identifier code assigned to the booster pad product."){record_delimiter}
("entity"{tuple_delimiter}"A Booster adds absorbency to a disposable undergarment..."{tuple_delimiter}"Description"{tuple_delimiter}"Provides details about the booster pad's absorbency, size options, adhesive backing, and stacking ability."){record_delimiter}
("entity"{tuple_delimiter}"Y"{tuple_delimiter}"Recommend"{tuple_delimiter}"Indicates the product is recommended for customers."){record_delimiter}
("entity"{tuple_delimiter}"100000"{tuple_delimiter}"Stock"{tuple_delimiter}"Represents a large available inventory of the product."){record_delimiter}
("entity"{tuple_delimiter}"Crinklz"{tuple_delimiter}"Brand"{tuple_delimiter}"The brand responsible for manufacturing the product."){record_delimiter}
("entity"{tuple_delimiter}"Shop For>Incontinence Products for Men>Booster Pads / Doublers, ..."{tuple_delimiter}"Category"{tuple_delimiter}"Detailed category classification including gender-specific use, featured products, and catalog placements."){record_delimiter}
("entity"{tuple_delimiter}"2727"{tuple_delimiter}"Sku"{tuple_delimiter}"The SKU code used to identify the product variation."){record_delimiter}
("entity"{tuple_delimiter}"Case/60 (4/15s) - Best Value!"{tuple_delimiter}"Package"{tuple_delimiter}"Describes the packaging unit including quantity and grouping."){record_delimiter}
("entity"{tuple_delimiter}"M"{tuple_delimiter}"Size"{tuple_delimiter}"Medium size specification for the booster pad."){record_delimiter}
("entity"{tuple_delimiter}"Original"{tuple_delimiter}"Style"{tuple_delimiter}"Represents the original version or design of the product."){record_delimiter}
("entity"{tuple_delimiter}"29.7"{tuple_delimiter}"Weight"{tuple_delimiter}"Product's weight in unspecified units, likely ounces."){record_delimiter}
("entity"{tuple_delimiter}"134.99"{tuple_delimiter}"Price"{tuple_delimiter}"List price in USD for a case of the booster pads."){record_delimiter}
("entity"{tuple_delimiter}"Backsheet: Smooth Plastic"{tuple_delimiter}"Material"{tuple_delimiter}"Specifies the material used in constructing the product’s backsheet."){record_delimiter}
("entity"{tuple_delimiter}"Leak Guards: Yes; Elastic Waistband: Front & Rear; Refastenable Tabs: Adhesive; Odor Control: Excellent; Absorbency: Maximum; Absorbent Zone: 13 x 15 x 7 in. Full 26 in."{tuple_delimiter}"Feature"{tuple_delimiter}"List of technical and comfort features for the booster pad, including leak guards and absorbency."){record_delimiter}
("entity"{tuple_delimiter}"Excellent; Maximum"{tuple_delimiter}"Benefit"{tuple_delimiter}"Describes the key customer benefits like odor control and absorbency level."){record_delimiter}
("entity"{tuple_delimiter}"/globalassets/product-assets/crinklz/d143-crinklz-briefs/png/crinklz-original-front-package.png"{tuple_delimiter}"Media"{tuple_delimiter}"Path to the main product image used for display."){record_delimiter}
("entity"{tuple_delimiter}"Overnight"{tuple_delimiter}"UseCase"{tuple_delimiter}"Intended usage scenario for overnight absorbency."){record_delimiter}
("entity"{tuple_delimiter}"Women, Men, Youth"{tuple_delimiter}"UserType"{tuple_delimiter}"Target demographics including women, men, and youth."){record_delimiter}
("entity"{tuple_delimiter}"Urinary, Bowel, Urinary+Bowel"{tuple_delimiter}"IncontinenceType"{tuple_delimiter}"Types of incontinence the product is designed to address."){record_delimiter}
("entity"{tuple_delimiter}"Absorbency Sort Integer: 30 oz.; Fits Weight: 29 - 43 in.; Hip Size: 29 - 43 in.; Waist Size: 29 - 43 in.; Fits Waists: 29 to 36 in., 37 to 48 in.; Fits Hips: 29 to 36 in., 37 to 48 in.; Product Size: Medium, 29 - 43 in.; Model Number: 60500"{tuple_delimiter}"Specification"{tuple_delimiter}"Technical specifications including size range, weight, and absorbency."){record_delimiter}
("entity"{tuple_delimiter}"Premium"{tuple_delimiter}"PricePoint"{tuple_delimiter}"Indicates this product belongs to the premium pricing category."){record_delimiter}
("relationship"{tuple_delimiter}"D002-2727"{tuple_delimiter}"NorthShore EternaDry Diaper Booster Pads (Diaper Doublers)"{tuple_delimiter}"Product ID maps to the product name."{tuple_delimiter}"identity mapping"{tuple_delimiter}10){record_delimiter}
("relationship"{tuple_delimiter}"D002-2727"{tuple_delimiter}"A Booster adds absorbency to a disposable undergarment..."{tuple_delimiter}"Product ID has a detailed product description."{tuple_delimiter}"describes product"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"D002-2727"{tuple_delimiter}"Y"{tuple_delimiter}"Product is recommended based on the recommend field."{tuple_delimiter}"recommendation status"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"D002-2727"{tuple_delimiter}"100000"{tuple_delimiter}"Product has stock availability value of 100000."{tuple_delimiter}"inventory status"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"D002-2727"{tuple_delimiter}"Crinklz"{tuple_delimiter}"Crinklz is the brand that manufactures this product."{tuple_delimiter}"manufacturer relationship"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"D002-2727"{tuple_delimiter}"Shop For>Incontinence Products for Men>Booster Pads / Doublers, ..."{tuple_delimiter}"Product is categorized under multiple incontinence-related classifications."{tuple_delimiter}"product categorization"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"D002-2727"{tuple_delimiter}"2727"{tuple_delimiter}"SKU code linked to the product."{tuple_delimiter}"product SKU"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"D002-2727"{tuple_delimiter}"Case/60 (4/15s) - Best Value!"{tuple_delimiter}"Product is sold in package of 60 divided in 4 sets of 15."{tuple_delimiter}"packaging format"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"D002-2727"{tuple_delimiter}"M"{tuple_delimiter}"Product is medium size."{tuple_delimiter}"size specification"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"D002-2727"{tuple_delimiter}"Original"{tuple_delimiter}"This is the original style version."{tuple_delimiter}"style attribute"{tuple_delimiter}6){record_delimiter}
("relationship"{tuple_delimiter}"D002-2727"{tuple_delimiter}"29.7"{tuple_delimiter}"Product weighs 29.7 units."{tuple_delimiter}"weight information"{tuple_delimiter}6){record_delimiter}
("relationship"{tuple_delimiter}"D002-2727"{tuple_delimiter}"134.99"{tuple_delimiter}"Product list price is $134.99."{tuple_delimiter}"price assignment"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"D002-2727"{tuple_delimiter}"Backsheet: Smooth Plastic"{tuple_delimiter}"Material used in product's construction is smooth plastic."{tuple_delimiter}"material specification"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"D002-2727"{tuple_delimiter}"Leak Guards: Yes; Elastic Waistband: Front & Rear; ..."{tuple_delimiter}"Product features include leak guards, tabs, waistband, etc."{tuple_delimiter}"feature list"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"D002-2727"{tuple_delimiter}"Excellent; Maximum"{tuple_delimiter}"Describes top-tier benefits like odor control and absorbency."{tuple_delimiter}"customer benefit"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"D002-2727"{tuple_delimiter}"/globalassets/product-assets/crinklz/d143-crinklz-briefs/png/crinklz-original-front-package.png"{tuple_delimiter}"Primary image asset for this product."{tuple_delimiter}"media attachment"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"D002-2727"{tuple_delimiter}"Overnight"{tuple_delimiter}"Product is intended for overnight usage."{tuple_delimiter}"use case"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"D002-2727"{tuple_delimiter}"Women, Men, Youth"{tuple_delimiter}"Product is suitable for women, men, and youth."{tuple_delimiter}"user demographic"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"D002-2727"{tuple_delimiter}"Urinary, Bowel, Urinary+Bowel"{tuple_delimiter}"Product addresses all common types of incontinence."{tuple_delimiter}"incontinence coverage"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"D002-2727"{tuple_delimiter}"Absorbency Sort Integer: 30 oz.; Fits Weight: 29 - 43 in.; ..."{tuple_delimiter}"Detailed technical specs for sizing, absorbency, and fit."{tuple_delimiter}"product specifications"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"D002-2727"{tuple_delimiter}"Premium"{tuple_delimiter}"Product is positioned as premium in the market."{tuple_delimiter}"price tier"{tuple_delimiter}7){record_delimiter}
("content_keywords"{tuple_delimiter}"incontinence care, booster pads, product specifications, premium absorbency, adult diapers, Crinklz brand"){completion_delimiter}
#############################"""
]

PROMPTS[
    "summarize_entity_descriptions"
] = """You are a helpful assistant responsible for generating a comprehensive summary of the data provided below.
Given one or two entities, and a list of descriptions, all related to the same entity or group of entities.
Please concatenate all of these into a single, comprehensive description. Make sure to include information collected from all the descriptions.
If the provided descriptions are contradictory, please resolve the contradictions and provide a single, coherent summary.
Make sure it is written in third person, and include the entity names so we the have full context.
Use {language} as output language.

#######
---Data---
Entities: {entity_name}
Description List: {description_list}
#######
Output:
"""

PROMPTS["entity_continue_extraction"] = """
MANY entities and relationships were missed in the last extraction.

---Remember Steps---

1. Identify all entities. For each identified entity, extract the following information:
- entity_name: Name of the entity, use same language as input text. If English, capitalized the name.
- entity_type: One of the following types: [{entity_types}]
- entity_description: Comprehensive description of the entity's attributes and activities
Format each entity as ("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_description>)

2. From the entities identified in step 1, identify all pairs of (source_entity, target_entity) that are *clearly related* to each other.
For each pair of related entities, extract the following information:
- source_entity: name of the source entity, as identified in step 1
- target_entity: name of the target entity, as identified in step 1
- relationship_description: explanation as to why you think the source entity and the target entity are related to each other
- relationship_strength: a numeric score indicating strength of the relationship between the source entity and target entity
- relationship_keywords: one or more high-level key words that summarize the overarching nature of the relationship, focusing on concepts or themes rather than specific details
Format each relationship as ("relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_description>{tuple_delimiter}<relationship_keywords>{tuple_delimiter}<relationship_strength>)

3. Identify high-level key words that summarize the main concepts, themes, or topics of the entire text. These should capture the overarching ideas present in the document.
Format the content-level key words as ("content_keywords"{tuple_delimiter}<high_level_keywords>)

4. Return output in {language} as a single list of all the entities and relationships identified in steps 1 and 2. Use **{record_delimiter}** as the list delimiter.

5. When finished, output {completion_delimiter}

---Output---

Add them below using the same format:\n
""".strip()

PROMPTS["entity_if_loop_extraction"] = """
---Goal---'

It appears some entities may have still been missed.

---Output---

Answer ONLY by `YES` OR `NO` if there are still entities that need to be added.
""".strip()

PROMPTS["fail_response"] = (
    "Sorry, I'm not able to provide an answer to that question.[no-context]"
)

PROMPTS["rag_response"] = """---Role---

You are a helpful assistant responding to user query about Knowledge Graph and Document Chunks provided in JSON format below.


---Goal---

Generate a concise response based on Knowledge Base and follow Response Rules, considering both the conversation history and the current query. Summarize all information in the provided Knowledge Base, and incorporating general knowledge relevant to the Knowledge Base. Do not include information not provided by Knowledge Base.

When handling relationships with timestamps:
1. Each relationship has a "created_at" timestamp indicating when we acquired this knowledge
2. When encountering conflicting relationships, consider both the semantic content and the timestamp
3. Don't automatically prefer the most recently created relationships - use judgment based on the context
4. For time-specific queries, prioritize temporal information in the content before considering creation timestamps

---Conversation History---
{history}

---Knowledge Graph and Document Chunks---
{context_data}

---Response Rules---

- Target format and length: {response_type}
- Use markdown formatting with appropriate section headings
- Please respond in the same language as the user's question.
- Ensure the response maintains continuity with the conversation history.
- List up to 5 most important reference sources at the end under "References" section. Clearly indicating whether each source is from Knowledge Graph (KG) or Document Chunks (DC), and include the file path if available, in the following format: [KG/DC] file_path
- If you don't know the answer, just say so.
- Do not make anything up. Do not include information not provided by the Knowledge Base.
- Addtional user prompt: {user_prompt}

Response:"""

PROMPTS["keywords_extraction"] = """---Role---

You are a helpful assistant tasked with identifying both high-level and low-level keywords in the user's query and conversation history.

---Goal---

Given the query and conversation history, list both high-level and low-level keywords. High-level keywords focus on overarching concepts or themes, while low-level keywords focus on specific entities, details, or concrete terms.

---Instructions---

- Consider both the current query and relevant conversation history when extracting keywords
- Output the keywords in JSON format, it will be parsed by a JSON parser, do not add any extra content in output
- The JSON should have two keys:
  - "high_level_keywords" for overarching concepts or themes
  - "low_level_keywords" for specific entities or details

######################
---Examples---
######################
{examples}

#############################
---Real Data---
######################
Conversation History:
{history}

Current Query: {query}
######################
The `Output` should be human text, not unicode characters. Keep the same language as `Query`.
Output:

"""

PROMPTS["keywords_extraction_examples"] = [
    """Example 1:

Query: "How does international trade influence global economic stability?"
################
Output:
{
  "high_level_keywords": ["International trade", "Global economic stability", "Economic impact"],
  "low_level_keywords": ["Trade agreements", "Tariffs", "Currency exchange", "Imports", "Exports"]
}
#############################""",
    """Example 2:

Query: "What are the environmental consequences of deforestation on biodiversity?"
################
Output:
{
  "high_level_keywords": ["Environmental consequences", "Deforestation", "Biodiversity loss"],
  "low_level_keywords": ["Species extinction", "Habitat destruction", "Carbon emissions", "Rainforest", "Ecosystem"]
}
#############################""",
    """Example 3:

Query: "What is the role of education in reducing poverty?"
################
Output:
{
  "high_level_keywords": ["Education", "Poverty reduction", "Socioeconomic development"],
  "low_level_keywords": ["School access", "Literacy rates", "Job training", "Income inequality"]
}
#############################""",
]

PROMPTS["naive_rag_response"] = """---Role---

You are a helpful assistant responding to user query about Document Chunks provided provided in JSON format below.

---Goal---

Generate a concise response based on Document Chunks and follow Response Rules, considering both the conversation history and the current query. Summarize all information in the provided Document Chunks, and incorporating general knowledge relevant to the Document Chunks. Do not include information not provided by Document Chunks.

When handling content with timestamps:
1. Each piece of content has a "created_at" timestamp indicating when we acquired this knowledge
2. When encountering conflicting information, consider both the content and the timestamp
3. Don't automatically prefer the most recent content - use judgment based on the context
4. For time-specific queries, prioritize temporal information in the content before considering creation timestamps

---Conversation History---
{history}

---Document Chunks(DC)---
{content_data}

---Response Rules---

- Target format and length: {response_type}
- Use markdown formatting with appropriate section headings
- Please respond in the same language as the user's question.
- Ensure the response maintains continuity with the conversation history.
- List up to 5 most important reference sources at the end under "References" section. Clearly indicating each source from Document Chunks(DC), and include the file path if available, in the following format: [DC] file_path
- If you don't know the answer, just say so.
- Do not include information not provided by the Document Chunks.
- Addtional user prompt: {user_prompt}

Response:"""

# TODO: deprecated
PROMPTS[
    "similarity_check"
] = """Please analyze the similarity between these two questions:

Question 1: {original_prompt}
Question 2: {cached_prompt}

Please evaluate whether these two questions are semantically similar, and whether the answer to Question 2 can be used to answer Question 1, provide a similarity score between 0 and 1 directly.

Similarity score criteria:
0: Completely unrelated or answer cannot be reused, including but not limited to:
   - The questions have different topics
   - The locations mentioned in the questions are different
   - The times mentioned in the questions are different
   - The specific individuals mentioned in the questions are different
   - The specific events mentioned in the questions are different
   - The background information in the questions is different
   - The key conditions in the questions are different
1: Identical and answer can be directly reused
0.5: Partially related and answer needs modification to be used
Return only a number between 0-1, without any additional content.
"""