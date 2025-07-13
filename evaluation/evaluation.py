from rouge_score import rouge_scorer

def evaluate_summary(generated, reference):
    scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
    scores = scorer.score(reference, generated)
    return scores['rougeL'].fmeasure

generated = """Onam is Kerala's biggest party—a ten-day harvest festival in August/September that everyone joins in on, regardless of religion.  It's all about celebrating their culture and history. The story behind it is super cool:  a super popular, fair King Mahabali got tricked by a god (in disguise!) and banished, but was allowed to visit his people once a year, which is what Onam celebrates. It's a time of joy, unity, and remembering a beloved king."""
reference = """Onam is the most important and popular festival celebrated in the Indian state of Kerala. It is a vibrant harvest festival that usually falls in the Malayalam month of Chingam (August–September) and lasts for ten days. Onam is deeply rooted in Kerala’s culture and heritage and is celebrated by people of all religions and communities, making it a symbol of unity, tradition, and joy.

The legend behind Onam is based on the mythical story of King Mahabali, a just and generous ruler who was loved by his people. According to Hindu mythology, the gods became jealous of Mahabali’s popularity and sought the help of Lord Vishnu. Vishnu took the form of a dwarf Brahmin named Vamana and visited Mahabali. He requested three paces of land, and when the king agreed, Vamana grew in size and covered the entire universe in two steps. For the third step, Mahabali offered his head. Touched by his devotion and humility, Lord Vishnu granted him the boon to visit his people once a year — and this annual visit is celebrated as Onam."""
score = evaluate_summary(generated, reference)
print(f"ROUGE-L F1 Score: {score:.4f}")