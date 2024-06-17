# Langchain Customer service

Automatically reply to customers and identify important tags in customer reviews.

## Workflow
The input to the system includes the original review and the user's rating for the product. The review is then translated into English, appropriate tags are identified from the review and finally, an apt response is generated for the customer in the language they used for the original review.

<img align="centre" alt="Good Example" width="800" src="https://github.com/akashsp7/Langchain-Customer_service/blob/main/images/Customer%20review_cropped.png?raw=true">

## A good example
Here the system correctly identified tags like dainty and well-made as well as appropriately thanked the customer for its review in a natural manner.

<img align="centre" alt="Good Example" width="800" src="https://github.com/akashsp7/Langchain-Customer_service/blob/main/images/good_performance.png?raw=true">

## Translated example
Here, the original review was posted in Hindi and OP mentioned how there was a small issue with the clasps, thus earning the necklace 4 stars. The system acknowledged this issue in the tags as well as apologized for it.

<img align="centre" alt="Translated" width="800" src="https://github.com/akashsp7/Langchain-Customer_service/blob/main/images/translated.png?raw=true">

## Bad Example
Here, as opposed to the previous case, the system did not record the tags in English, but in the original language of the review.

<img align="centre" alt="Bad Example" width="800" src="https://github.com/akashsp7/Langchain-Customer_service/blob/main/images/failed_performance.png?raw=true">

