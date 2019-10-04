from google.cloud.language_v1 import enums
import os

'''
# Please set up  your own GOOGLE_APPLICATION_CREDENTIALS json file, example ./my_google_credentials.json
gaCredentials = r"*********.json"
This application demonstrates a voice file 
can be transformed to text in a better result after applying a noise reduction. 
example:
enText = "Joanne Rowling, who writes under the pen names J. K. Rowling and Robert Galbraith, is a British novelist and screenwriter who wrote the Harry Potter fantasy series"
the result with highest Salience: we find that Joanne Rowling, Rowling, novelist, Robert Galbraith are refer to one thing.
Representative name for the entity: Joanne Rowling
Entity type: PERSON
Salience score: 0.813799262046814
wikipedia_url: https://en.wikipedia.org/wiki/J._K._Rowling
mid: /m/042xh
Mention text: Joanne Rowling
Mention type: PROPER
Mention text: Rowling
Mention type: PROPER
Mention text: novelist
Mention type: COMMON
Mention text: Robert Galbraith
Mention type: PROPER
'''






#gcs_uri = 'gs://cloud-samples-data/language/president.txt'
def sample_analyze_entities(text_content,language):
    """
    Analyzing Entities in a String
    Args:
      text_content The text content to analyze
      language: The language of the text
    """

    client = language_v1.LanguageServiceClient()

    # text_content = 'California is a state.'

    # Available types: PLAIN_TEXT, HTML
    type_ = enums.Document.Type.PLAIN_TEXT

    # Optional. If not specified, the language is automatically detected.
    # For list of supported languages:

    #language = "zh-Hant"
    document = {"content": text_content, "type": type_, "language": language}

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = enums.EncodingType.UTF8

    response = client.analyze_entities(document, encoding_type=encoding_type)
    # Loop through entitites returned from the API
    for entity in response.entities:
        print(u"Representative name for the entity: {}".format(entity.name))
        # Get entity type, e.g. PERSON, LOCATION, ADDRESS, NUMBER, et al
        print(u"Entity type: {}".format(enums.Entity.Type(entity.type).name))
        # Get the salience score associated with the entity in the [0, 1.0] range
        print(u"Salience score: {}".format(entity.salience))
        # Loop over the metadata associated with entity. For many known entities,
        # the metadata is a Wikipedia URL (wikipedia_url) and Knowledge Graph MID (mid).
        # Some entity types may have additional metadata, e.g. ADDRESS entities
        # may have metadata for the address street_name, postal_code, et al.
        for metadata_name, metadata_value in entity.metadata.items():
            print(u"{}: {}".format(metadata_name, metadata_value))
        # Loop over the mentions of this entity in the input document.
        # The API currently supports proper noun mentions.
        for mention in entity.mentions:
            print(u"Mention text: {}".format(mention.text.content))
            # Get the mention type, e.g. PROPER for proper noun
            print(
                u"Mention type: {}".format(enums.EntityMention.Type(mention.type).name)
            )
        print("="*100)
    # Get the language of the text, which will be the same as
    # the language specified in the request or, if not specified,
    # the automatically-detected language.
    print(u"Language of the text: {}".format(response.language))

gaCredentials = r""           
os.environ['GOOGLE_APPLICATION_CREDENTIALS']= gaCredentials
enText = "Joanne Rowling, who writes under the pen names J. K. Rowling and Robert Galbraith, is a British novelist and screenwriter who wrote the Harry Potter fantasy series"
language = "en"  # specify your text language, for the language code, please refer to https://cloud.google.com/natural-language/docs/languages
sample_analyze_entities(enText,language)
