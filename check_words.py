#!/usr/bin/env python3
"""
Script to check if words from glossary_words_sentence_usage.csv 
exist in Glossary.md file and store unfound words in unfound.txt
"""

import csv
import re

def extract_words_from_glossary(glossary_file):
    """Extract all words from Glossary.md file that are in **word** format"""
    words = set()
    all_words = []  # Track all words including duplicates
    
    try:
        with open(glossary_file, 'r', encoding='utf-8') as file:
            content = file.read()
            # Find all words in **word** format
            pattern = r'\*\*([^*]+)\*\*'
            matches = re.findall(pattern, content)
            # Convert to lowercase for case-insensitive comparison
            for word in matches:
                clean_word = word.lower().strip()
                all_words.append(clean_word)
                words.add(clean_word)
    except FileNotFoundError:
        print(f"Error: {glossary_file} not found!")
        return set(), []
    except Exception as e:
        print(f"Error reading {glossary_file}: {e}")
        return set(), []
    
    return words, all_words

def extract_words_from_csv(csv_file):
    """Extract words from the first column of the CSV file"""
    words = []
    unique_words = set()
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            # Skip header row
            next(reader, None)
            
            for row in reader:
                if row:  # Check if row is not empty
                    word = row[0].strip().lower()  # First column, lowercase
                    if word:  # Check if word is not empty
                        words.append(word)
                        unique_words.add(word)
    except FileNotFoundError:
        print(f"Error: {csv_file} not found!")
        return [], set()
    except Exception as e:
        print(f"Error reading {csv_file}: {e}")
        return [], set()
    
    return words, unique_words

def find_duplicates(word_list):
    """Find duplicate words in a list"""
    word_count = {}
    duplicates = {}
    
    for word in word_list:
        word_count[word] = word_count.get(word, 0) + 1
    
    for word, count in word_count.items():
        if count > 1:
            duplicates[word] = count
    
    return duplicates

def find_unfound_words(csv_words, glossary_words):
    """Find words that are in CSV but not in Glossary"""
    unfound = []
    
    for word in csv_words:
        if word not in glossary_words:
            unfound.append(word)
    
    return unfound

def save_unfound_words(unfound_words, output_file, csv_duplicates, glossary_duplicates, csv_total, glossary_total, csv_unique, glossary_unique):
    """Save unfound words and duplicate analysis to a text file"""
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write("WORD ANALYSIS REPORT\n")
            file.write("=" * 50 + "\n\n")
            
            # Summary statistics
            file.write("SUMMARY STATISTICS:\n")
            file.write("-" * 20 + "\n")
            file.write(f"Total words in CSV: {csv_total}\n")
            file.write(f"Unique words in CSV: {csv_unique}\n")
            file.write(f"Duplicates in CSV: {csv_total - csv_unique}\n")
            file.write(f"Total words in Glossary: {glossary_total}\n")
            file.write(f"Unique words in Glossary: {glossary_unique}\n")
            file.write(f"Duplicates in Glossary: {glossary_total - glossary_unique}\n")
            file.write(f"Unfound words: {len(unfound_words)}\n\n")
            
            # CSV Duplicates
            if csv_duplicates:
                file.write("DUPLICATES IN CSV FILE:\n")
                file.write("-" * 25 + "\n")
                for word, count in sorted(csv_duplicates.items()):
                    file.write(f"{word}: {count} occurrences\n")
                file.write(f"\nTotal duplicate entries in CSV: {sum(csv_duplicates.values()) - len(csv_duplicates)}\n\n")
            else:
                file.write("No duplicates found in CSV file.\n\n")
            
            # Glossary Duplicates
            if glossary_duplicates:
                file.write("DUPLICATES IN GLOSSARY FILE:\n")
                file.write("-" * 28 + "\n")
                for word, count in sorted(glossary_duplicates.items()):
                    file.write(f"{word}: {count} occurrences\n")
                file.write(f"\nTotal duplicate entries in Glossary: {sum(glossary_duplicates.values()) - len(glossary_duplicates)}\n\n")
            else:
                file.write("No duplicates found in Glossary file.\n\n")
            
            # Unfound words
            if unfound_words:
                file.write("WORDS FOUND IN CSV BUT NOT IN GLOSSARY:\n")
                file.write("-" * 40 + "\n")
                for i, word in enumerate(unfound_words, 1):
                    file.write(f"{i}. {word}\n")
            else:
                file.write("✅ All words from CSV were found in Glossary.md!\n")
                
    except Exception as e:
        print(f"Error writing to {output_file}: {e}")

def main():
    # File paths
    csv_file = "glossary_words_sentence_usage.csv"
    glossary_file = "Glossary.md"
    output_file = "unfound.txt"
    
    print("Starting word comparison...")
    print("=" * 60)
    
    # Extract words from both files
    print(f"📖 Reading words from {glossary_file}...")
    glossary_words, all_glossary_words = extract_words_from_glossary(glossary_file)
    glossary_duplicates = find_duplicates(all_glossary_words)
    print(f"   Found {len(all_glossary_words)} total words in Glossary.md")
    print(f"   Found {len(glossary_words)} unique words in Glossary.md")
    if glossary_duplicates:
        print(f"   Found {len(glossary_duplicates)} duplicate words in Glossary.md")
    
    print(f"\n📊 Reading words from {csv_file}...")
    all_csv_words, csv_words = extract_words_from_csv(csv_file)
    csv_duplicates = find_duplicates(all_csv_words)
    print(f"   Found {len(all_csv_words)} total words in CSV file")
    print(f"   Found {len(csv_words)} unique words in CSV file")
    if csv_duplicates:
        print(f"   Found {len(csv_duplicates)} duplicate words in CSV file")
    
    # Target count check
    expected_total = 1055
    print(f"\n🎯 Target word count: {expected_total}")
    if len(all_csv_words) == expected_total:
        print(f"   ✅ CSV contains exactly {expected_total} words!")
    else:
        print(f"   ⚠️  CSV contains {len(all_csv_words)} words (expected {expected_total})")
    
    # Find unfound words
    print(f"\n🔍 Comparing words...")
    unfound_words = find_unfound_words(csv_words, glossary_words)
    
    # Save results
    print(f"\n💾 Saving results to {output_file}...")
    save_unfound_words(unfound_words, output_file, csv_duplicates, glossary_duplicates, 
                      len(all_csv_words), len(all_glossary_words), len(csv_words), len(glossary_words))
    
    # Print detailed summary
    print("\n" + "=" * 60)
    print("📋 DETAILED SUMMARY:")
    print("=" * 60)
    print(f"CSV File Analysis:")
    print(f"  • Total words: {len(all_csv_words)}")
    print(f"  • Unique words: {len(csv_words)}")
    print(f"  • Duplicate entries: {len(all_csv_words) - len(csv_words)}")
    print(f"  • Duplicate word types: {len(csv_duplicates)}")
    
    print(f"\nGlossary File Analysis:")
    print(f"  • Total words: {len(all_glossary_words)}")
    print(f"  • Unique words: {len(glossary_words)}")
    print(f"  • Duplicate entries: {len(all_glossary_words) - len(glossary_words)}")
    print(f"  • Duplicate word types: {len(glossary_duplicates)}")
    
    print(f"\nComparison Results:")
    print(f"  • Words in CSV but not in Glossary: {len(unfound_words)}")
    
    if csv_duplicates:
        print(f"\n🔄 CSV Duplicates found:")
        for word, count in sorted(list(csv_duplicates.items())[:5]):
            print(f"     • '{word}' appears {count} times")
        if len(csv_duplicates) > 5:
            print(f"     ... and {len(csv_duplicates) - 5} more duplicates")
    
    if glossary_duplicates:
        print(f"\n🔄 Glossary Duplicates found:")
        for word, count in sorted(list(glossary_duplicates.items())[:5]):
            print(f"     • '{word}' appears {count} times")
        if len(glossary_duplicates) > 5:
            print(f"     ... and {len(glossary_duplicates) - 5} more duplicates")
    
    if unfound_words:
        print(f"\n❌ Unfound words (first 5):")
        for word in unfound_words[:5]:
            print(f"     • {word}")
        if len(unfound_words) > 5:
            print(f"     ... and {len(unfound_words) - 5} more")
        print(f"\n📄 Complete results saved to {output_file}")
    else:
        print("\n✅ All words found in Glossary.md!")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
