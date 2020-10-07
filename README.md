# Vulnerable Customers
How can NLP be used to identify vulnerable customers under FCA guidelines
4 key drivers of vulnerability:
1. Health – disabilities or illnesses that affect the ability to carry out day-to-day tasks
2. Life Events – major life events such as bereavement, job loss or relationship breakdown
3. Resilience – low ability to withstand financial or emotional shocks
4. Capability – low knowledge of financial matters or low confidence in managing money (financial capability) and low capability in other relevant areas such as literacy, or digital skills

Which we can normalise into distinct topics, e.g.:
1. Death
2. Redundancy
3. Furlough
etc...

Potential approaches:
1. Bag-of-Words: will need enough training data for us to come to some sensible features. This will essentially be a goal-seeking exercise because sensible features will need to include synonyms of the topic at hand.
2. Similarity measure: use a WordNet based similarity measure to monitor stream of text for mention of words close in meaning to these topics, ie. synonyms.

Let's start with the simpler option: approach 2, as this requires no training data.
