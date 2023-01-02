import collator, merger, author

# if no arguments, run interactively

# select collator
# apply collator arguments
selected_collator: collator.Collator = Collator()
# apply collator
authors: list[author.Author] = selected_collator.run()

# select merger
# apply merger arguments
selected_merger: merger.Merger = Merger()
# apply merger
results: dict[str, str] = selected_merger.run(authors)

# save file