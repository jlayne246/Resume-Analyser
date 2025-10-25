from services.extraction import PDF

if __name__ == "__main__":
    source = "samples/sampleMargaret.pdf"
    pdf=PDF(source)
    option = input("Pick an option\n1: Count pages\n2: Extract text\n3: Extract clean text\n4: Make summary\n5: Get Bert\n\nEnter option number: ")
    if option == '1':
        print(f"Number of pages: {pdf.count_pages()}")
    elif option == '2':
        print("Extracted Text:")
        print(pdf.extract_text())
    elif option == '3':
        print("Extracted Text (clean):")
        print(pdf.extract_clean_text())
    elif option == '4':
        print("Named Entities in the Document:")
        pdf.make_summary()
    elif option == '5':
        print("BERT Model Output:")
        outputs = pdf.test_bert()
        print(outputs)