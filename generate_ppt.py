"""
generate_ppt.py
Generates a 15-slide PowerPoint presentation (.pptx) for the
Fake Review Detection System college project.
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Color Palette
    DARK_BLUE = RGBColor(15, 23, 42)      # #0f172a
    ACCENT_BLUE = RGBColor(37, 99, 235)   # #2563eb
    TEXT_MAIN = RGBColor(30, 41, 59)      # #1e293b
    TEXT_MUTED = RGBColor(100, 116, 139)  # #64748b
    BG_LIGHT = RGBColor(248, 250, 252)    # #f8fafc
    CARD_BG = RGBColor(255, 255, 255)     # #ffffff
    BORDER_COLOR = RGBColor(226, 232, 240)# #e2e8f0
    GREEN_COLOR = RGBColor(22, 163, 74)   # #16a34a
    RED_COLOR = RGBColor(220, 38, 38)     # #dc2626

    blank_slide_layout = prs.slide_layouts[6]

    def add_header(slide, title_text, category_text="FAKE REVIEW DETECTION SYSTEM"):
        # Top banner background
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.15))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = DARK_BLUE
        top_bar.line.fill.background()

        # Category tag
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.18), Inches(11.5), Inches(0.3))
        cat_tf = cat_box.text_frame
        cat_tf.word_wrap = True
        cat_p = cat_tf.paragraphs[0]
        cat_p.text = category_text.upper()
        cat_p.font.size = Pt(10)
        cat_p.font.bold = True
        cat_p.font.color.rgb = ACCENT_BLUE

        # Slide Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.42), Inches(11.5), Inches(0.6))
        title_tf = title_box.text_frame
        title_tf.word_wrap = True
        title_p = title_tf.paragraphs[0]
        title_p.text = title_text
        title_p.font.size = Pt(22)
        title_p.font.bold = True
        title_p.font.color.rgb = RGBColor(255, 255, 255)

    def set_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_LIGHT
        bg.line.fill.background()

    def add_notes(slide, notes_text):
        notes_slide = slide.notes_slide
        text_frame = notes_slide.notes_text_frame
        text_frame.text = notes_text

    # ==========================================
    # SLIDE 1: Title Slide
    # ==========================================
    s1 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s1)

    # Main Hero Card
    hero = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(1.0), Inches(10.933), Inches(5.5))
    hero.fill.solid()
    hero.fill.fore_color.rgb = CARD_BG
    hero.line.color.rgb = BORDER_COLOR
    hero.line.width = Pt(1.5)

    tb = s1.shapes.add_textbox(Inches(1.8), Inches(1.5), Inches(9.733), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "COLLEGE MINI-PROJECT PRESENTATION"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = ACCENT_BLUE
    p.space_after = Pt(14)

    p2 = tf.add_paragraph()
    p2.text = "Fake Review Detection System"
    p2.font.size = Pt(32)
    p2.font.bold = True
    p2.font.color.rgb = DARK_BLUE
    p2.space_after = Pt(8)

    p3 = tf.add_paragraph()
    p3.text = "Using Deep Learning (Bidirectional LSTM) & Natural Language Processing"
    p3.font.size = Pt(18)
    p3.font.color.rgb = ACCENT_BLUE
    p3.space_after = Pt(28)

    p4 = tf.add_paragraph()
    p4.text = "Department of Computer Science & Engineering"
    p4.font.size = Pt(14)
    p4.font.bold = True
    p4.font.color.rgb = TEXT_MAIN
    p4.space_after = Pt(6)

    p5 = tf.add_paragraph()
    p5.text = "Presented by: Student Team / [Your Name]  |  Academic Year: 2025 - 2026"
    p5.font.size = Pt(13)
    p5.font.color.rgb = TEXT_MUTED

    add_notes(s1, "Welcome respected professors and evaluators. Today we present our project: Fake Review Detection System using Deep Learning and Natural Language Processing.")

    # ==========================================
    # SLIDE 2: Introduction & Motivation
    # ==========================================
    s2 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s2)
    add_header(s2, "1. Introduction & Real-World Motivation")

    card1 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2))
    card1.fill.solid()
    card1.fill.fore_color.rgb = CARD_BG
    card1.line.color.rgb = BORDER_COLOR
    tf1 = card1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "E-Commerce Reliance"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = DARK_BLUE
    p.space_after = Pt(12)

    bullets1 = [
        "93%+ of consumers read reviews before making an online purchase.",
        "Product star ratings directly determine e-commerce conversion rates.",
        "Consumer trust is heavily anchored to crowd-sourced feedback on Amazon, Flipkart, Yelp, and Google.",
        "Uninformed buyers risk financial loss and substandard goods."
    ]
    for b in bullets1:
        bp = tf1.add_paragraph()
        bp.text = "• " + b
        bp.font.size = Pt(13)
        bp.font.color.rgb = TEXT_MAIN
        bp.space_after = Pt(10)

    card2 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.2))
    card2.fill.solid()
    card2.fill.fore_color.rgb = CARD_BG
    card2.line.color.rgb = BORDER_COLOR
    tf2 = card2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "The Fraud Landscape"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = RED_COLOR
    p.space_after = Pt(12)

    bullets2 = [
        "Astroturfing: Paid agencies publish coordinated positive reviews to artificially boost rankings.",
        "Smear Campaigns: Competitors commission fake 1-star reviews to hurt business rivals.",
        "Human Limitation: Studies show ordinary consumers detect fake reviews at barely above chance (~54%).",
        "Need: Automated, explainable NLP systems that evaluate linguistic authenticity in real time."
    ]
    for b in bullets2:
        bp = tf2.add_paragraph()
        bp.text = "• " + b
        bp.font.size = Pt(13)
        bp.font.color.rgb = TEXT_MAIN
        bp.space_after = Pt(10)

    add_notes(s2, "Reviews influence billions of dollars in purchases annually. Because humans cannot reliably detect deceptive reviews, automated NLP systems are necessary.")

    # ==========================================
    # SLIDE 3: Problem Statement & Objectives
    # ==========================================
    s3 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s3)
    add_header(s3, "2. Problem Statement & Objectives")

    # Problem box
    prob_box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.733), Inches(1.6))
    prob_box.fill.solid()
    prob_box.fill.fore_color.rgb = CARD_BG
    prob_box.line.color.rgb = RED_COLOR
    prob_box.line.width = Pt(1.5)
    ptf = prob_box.text_frame
    ptf.word_wrap = True
    p = ptf.paragraphs[0]
    p.text = "PROBLEM STATEMENT"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = RED_COLOR
    p.space_after = Pt(4)
    p2 = ptf.add_paragraph()
    p2.text = "How can we accurately classify short, unstructured text reviews as Genuine or Fake in isolation (without relying on external account metadata or IP logs), while providing transparent, human-understandable explanations for the prediction?"
    p2.font.size = Pt(14)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_MAIN

    # 3 Objective Columns
    objs = [
        ("1. Sentiment-Aware NLP", "Clean review text while strictly preserving negation words ('not', 'never') that determine context.", ACCENT_BLUE),
        ("2. Bidirectional Sequence DL", "Deploy a Bidirectional LSTM neural network to analyze sentence semantics in both forward and reverse directions.", DARK_BLUE),
        ("3. Explainable AI & Clean UI", "Identify rule-based suspicious writing patterns and deliver results via a professional web dashboard.", GREEN_COLOR),
    ]
    for i, (otitle, odesc, ocolor) in enumerate(objs):
        x = Inches(0.8 + i * 4.0)
        ocard = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(3.4), Inches(3.733), Inches(3.4))
        ocard.fill.solid()
        ocard.fill.fore_color.rgb = CARD_BG
        ocard.line.color.rgb = BORDER_COLOR
        otf = ocard.text_frame
        otf.word_wrap = True
        op = otf.paragraphs[0]
        op.text = otitle
        op.font.size = Pt(16)
        op.font.bold = True
        op.font.color.rgb = ocolor
        op.space_after = Pt(12)
        op2 = otf.add_paragraph()
        op2.text = odesc
        op2.font.size = Pt(13)
        op2.font.color.rgb = TEXT_MAIN

    add_notes(s3, "Our objective is twofold: perform high-accuracy binary classification using Bidirectional LSTMs, and make the prediction explainable to users through heuristic pattern flags.")

    # ==========================================
    # SLIDE 4: Existing vs. Proposed System
    # ==========================================
    s4 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s4)
    add_header(s4, "3. Existing Systems vs. Proposed Solution")

    table_shape = s4.shapes.add_table(5, 3, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.0))
    table = table_shape.table

    table.columns[0].width = Inches(2.8)
    table.columns[1].width = Inches(4.4)
    table.columns[2].width = Inches(4.533)

    headers = ["Feature / Dimension", "Existing Systems (Traditional ML)", "Our Proposed System (BiLSTM + Heuristics)"]
    for col_idx, h in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = DARK_BLUE
        for p in cell.text_frame.paragraphs:
            p.font.bold = True
            p.font.size = Pt(13)
            p.font.color.rgb = RGBColor(255, 255, 255)

    rows_data = [
        ("Word Ordering", "Bag-of-Words / TF-IDF: ignores sequence context completely.", "Bidirectional LSTM: maintains forward & reverse sequential memory."),
        ("Negation Handling", "Standard stopwords drop 'not' & 'never', inverting sentiment.", "Custom stopword engine preserves all negation tokens."),
        ("Model Output", "Black-box classification probability without rationale.", "Dual Output: Neural confidence + Rule-based heuristic red flags."),
        ("User Interaction", "Command-line scripts or cluttered prototype dashboards.", "Clean, solid-color human-designed UI with one-click test cases.")
    ]
    for row_idx, row in enumerate(rows_data, start=1):
        for col_idx, text in enumerate(row):
            cell = table.cell(row_idx, col_idx)
            cell.text = text
            cell.fill.solid()
            cell.fill.fore_color.rgb = CARD_BG if row_idx % 2 == 1 else BG_LIGHT
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(12)
                p.font.color.rgb = TEXT_MAIN

    add_notes(s4, "Notice how traditional systems strip out negation words and disregard word order. Our BiLSTM captures full contextual meaning in both directions.")

    # ==========================================
    # SLIDE 5: System Architecture
    # ==========================================
    s5 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s5)
    add_header(s5, "4. High-Level System Architecture")

    steps = [
        ("1. Input & Validation", "User submits review text via Web UI (3 - 2,000 chars)", Inches(0.8)),
        ("2. Text Cleaner (NLP)", "Lowercasing, RegEx stripping, lemmatization, negation preservation", Inches(3.2)),
        ("3. Tokenizer & Padding", "Integer mapping, pre-padding to fixed 150-length matrix", Inches(5.6)),
        ("4. Dual Engine", "BiLSTM Model: P(Fake)\nHeuristic Analyzer: Flags", Inches(8.0)),
        ("5. Response & Display", "Confidence score, probability table, badge reasons", Inches(10.4)),
    ]
    for title, desc, x_pos in steps:
        step_card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x_pos, Inches(2.2), Inches(2.15), Inches(4.2))
        step_card.fill.solid()
        step_card.fill.fore_color.rgb = CARD_BG
        step_card.line.color.rgb = ACCENT_BLUE
        step_card.line.width = Pt(1.5)
        stf = step_card.text_frame
        stf.word_wrap = True
        sp = stf.paragraphs[0]
        sp.text = title
        sp.font.size = Pt(14)
        sp.font.bold = True
        sp.font.color.rgb = DARK_BLUE
        sp.space_after = Pt(10)
        sp2 = stf.add_paragraph()
        sp2.text = desc
        sp2.font.size = Pt(12)
        sp2.font.color.rgb = TEXT_MUTED

    add_notes(s5, "Our pipeline flows from client validation to Flask, then splits into our dual-engine: BiLSTM for sequence probability and Heuristic Analyzer for explainable pattern flags.")

    # ==========================================
    # SLIDE 6: Dataset Strategy & Design
    # ==========================================
    s6 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s6)
    add_header(s6, "5. Dataset Strategy & Linguistic Characteristics")

    c1 = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2))
    c1.fill.solid()
    c1.fill.fore_color.rgb = CARD_BG
    c1.line.color.rgb = BORDER_COLOR
    tf1 = c1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "Dataset Composition"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = DARK_BLUE
    p.space_after = Pt(10)

    b1 = [
        "Dataset File: dataset/reviews.csv (405 labeled review samples).",
        "Balanced Distribution: 50% Genuine Reviews (Label 0), 50% Fake Reviews (Label 1).",
        "Domain Diversity: Electronics, Home & Kitchen, Apparel, Office Equipment, Services.",
        "Stratified 80/20 Train-Test Split: 324 training reviews, 81 testing reviews (held-out)."
    ]
    for b in b1:
        bp = tf1.add_paragraph()
        bp.text = "• " + b
        bp.font.size = Pt(13)
        bp.font.color.rgb = TEXT_MAIN
        bp.space_after = Pt(8)

    c2 = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.2))
    c2.fill.solid()
    c2.fill.fore_color.rgb = CARD_BG
    c2.line.color.rgb = BORDER_COLOR
    tf2 = c2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "Linguistic Signatures"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = ACCENT_BLUE
    p.space_after = Pt(10)

    b2 = [
        "Genuine Reviews: Focus on tangible specifications, delivery timeframes, battery life, nuanced pros and cons.",
        "Fake Reviews: High density of superlatives ('miracle', 'best ever'), urgent calls to action ('BUY THIS NOW'), and lack of specific context.",
        "Negative Genuine Reviews: Critical reviews are included to train the model not to flag every negative review as fake."
    ]
    for b in b2:
        bp = tf2.add_paragraph()
        bp.text = "• " + b
        bp.font.size = Pt(13)
        bp.font.color.rgb = TEXT_MAIN
        bp.space_after = Pt(8)

    add_notes(s6, "We curated a balanced dataset that mirrors real-world linguistic traits: authentic reviews cite specific features and dates, while fake reviews exhibit promotional urgency.")

    # ==========================================
    # SLIDE 7: NLP Preprocessing Pipeline
    # ==========================================
    s7 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s7)
    add_header(s7, "6. NLP Preprocessing Pipeline")

    nlp_steps = [
        ("1. Lowercasing", "Standardizes all text to lowercase while retaining caps ratio metadata for heuristic inspection."),
        ("2. RegEx Cleaning", "Strips URLs (http/https), HTML markup tags, and non-alphanumeric noise."),
        ("3. Sentiment Preservation", "Custom filter removes generic stopwords but keeps negation tokens ('not', 'never', 'no', 'hardly')."),
        ("4. Lemmatization", "WordNetLemmatizer maps inflected words to root dictionary lemmas ('purchased' -> 'purchase')."),
        ("5. Integer Tokenization", "Maps unique vocabulary tokens into integer IDs using Keras Tokenizer (<OOV> for unseen words)."),
        ("6. Pre-Padding", "Pads sequences to fixed length of 150 tokens. Pre-padding preserves gradient flow in LSTMs.")
    ]
    for idx, (stitle, sdesc) in enumerate(nlp_steps):
        row = idx // 3
        col = idx % 3
        x = Inches(0.8 + col * 4.0)
        y = Inches(1.6 + row * 2.6)
        sc = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(3.733), Inches(2.3))
        sc.fill.solid()
        sc.fill.fore_color.rgb = CARD_BG
        sc.line.color.rgb = BORDER_COLOR
        stf = sc.text_frame
        stf.word_wrap = True
        p = stf.paragraphs[0]
        p.text = stitle
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = DARK_BLUE
        p.space_after = Pt(6)
        p2 = stf.add_paragraph()
        p2.text = sdesc
        p2.font.size = Pt(12)
        p2.font.color.rgb = TEXT_MAIN

    add_notes(s7, "A critical novelty in our NLP preprocessing is sentiment preservation. Generic stopword removers discard 'not', which distorts sentiment. We protect negation words.")

    # ==========================================
    # SLIDE 8: Deep Learning Architecture
    # ==========================================
    s8 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s8)
    add_header(s8, "7. Bidirectional LSTM Neural Network")

    # Left: Layer Architecture Table
    t_shape = s8.shapes.add_table(7, 3, Inches(0.8), Inches(1.6), Inches(7.5), Inches(5.2))
    t = t_shape.table
    t.columns[0].width = Inches(3.0)
    t.columns[1].width = Inches(2.2)
    t.columns[2].width = Inches(2.3)

    layers = [
        ("Layer (Type)", "Output Shape", "Param #"),
        ("1. Input (Padded Sequence)", "(None, 150)", "0"),
        ("2. Embedding (64-dim)", "(None, 150, 64)", "320,000"),
        ("3. SpatialDropout1D (0.3)", "(None, 150, 64)", "0"),
        ("4. Bidirectional LSTM (32)", "(None, 64)", "24,832"),
        ("5. Dense (ReLU) + Dropout", "(None, 32)", "2,080"),
        ("6. Dense (Sigmoid Output)", "(None, 1)", "33"),
    ]
    for r_idx, row in enumerate(layers):
        for c_idx, val in enumerate(row):
            cell = t.cell(r_idx, c_idx)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = DARK_BLUE if r_idx == 0 else (CARD_BG if r_idx % 2 == 1 else BG_LIGHT)
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(11)
                p.font.bold = (r_idx == 0)
                p.font.color.rgb = RGBColor(255, 255, 255) if r_idx == 0 else TEXT_MAIN

    # Right: Rationale Box
    r_box = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.6), Inches(1.6), Inches(3.933), Inches(5.2))
    r_box.fill.solid()
    r_box.fill.fore_color.rgb = CARD_BG
    r_box.line.color.rgb = BORDER_COLOR
    rtf = r_box.text_frame
    rtf.word_wrap = True
    p = rtf.paragraphs[0]
    p.text = "Why Bidirectional LSTM?"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_BLUE
    p.space_after = Pt(10)

    reasons = [
        "Bidirectional Context: Evaluates token meaning based on preceding and subsequent words.",
        "Handles Long-Range Memory: Overcomes vanishing gradients of standard RNNs.",
        "Compact Parameter Footprint: ~347k parameters enables rapid inference (<15ms per review) on standard CPU.",
        "SpatialDropout1D: Drops full 1D feature slices across text embeddings to enhance generalization."
    ]
    for r in reasons:
        rp = rtf.add_paragraph()
        rp.text = "• " + r
        rp.font.size = Pt(12)
        rp.font.color.rgb = TEXT_MAIN
        rp.space_after = Pt(8)

    add_notes(s8, "Our Bidirectional LSTM runs 32 units forward and 32 units backward, capturing contextual cues across both directions. Total parameters are around 347k.")

    # ==========================================
    # SLIDE 9: Training & Optimization
    # ==========================================
    s9 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s9)
    add_header(s9, "8. Model Training & Hyperparameters")

    cards_data = [
        ("Loss Function", "Binary Cross-Entropy", "Measures divergence between predicted probability and actual label (0 or 1)."),
        ("Optimizer", "Adam (lr=0.001)", "Adaptive learning rate with momentum for stable and rapid convergence."),
        ("Regularization", "SpatialDropout + Dropout", "30% dropout rates prevent co-adaptation and protect against overfitting."),
        ("EarlyStopping", "Patience = 4 epochs", "Monitors validation loss; automatically restores best weights."),
        ("Batch Size & Epochs", "Batch: 16 | Max: 30", "Small batch size provides beneficial stochastic gradient noise."),
        ("Model Persistence", ".keras & .pkl artifacts", "Model & tokenizer are saved to disk; zero retraining needed on app launch.")
    ]
    for idx, (ctitle, cval, cdesc) in enumerate(cards_data):
        row = idx // 3
        col = idx % 3
        x = Inches(0.8 + col * 4.0)
        y = Inches(1.6 + row * 2.6)
        c = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(3.733), Inches(2.3))
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = BORDER_COLOR
        ctf = c.text_frame
        ctf.word_wrap = True
        p = ctf.paragraphs[0]
        p.text = ctitle
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(4)
        p2 = ctf.add_paragraph()
        p2.text = cval
        p2.font.size = Pt(16)
        p2.font.bold = True
        p2.font.color.rgb = DARK_BLUE
        p2.space_after = Pt(6)
        p3 = ctf.add_paragraph()
        p3.text = cdesc
        p3.font.size = Pt(12)
        p3.font.color.rgb = TEXT_MAIN

    add_notes(s9, "We train with EarlyStopping and Adam optimizer. Once trained, the model is serialized so the Flask server loads it immediately on startup.")

    # ==========================================
    # SLIDE 10: Explainable AI & Heuristics
    # ==========================================
    s10 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s10)
    add_header(s10, "9. Explainable AI (XAI) & Pattern Heuristics")

    flags = [
        ("🚩 Promotional Language", "Detects urgency terms: 'buy now', 'must have', 'miracle product', 'click here', 'limited offer'."),
        ("🚩 Excessive Capitalization", "Flags reviews where over 25% of all words are written in ALL-CAPS (e.g. 'BEST PRODUCT EVER')."),
        ("🚩 Punctuation Abuse", "Detects repeated exclamation runs ('!!!') or question marks ('???') indicating false hype."),
        ("🚩 Consecutive Repetition", "Identifies identical repeated words and phrases ('great great', '5 stars 5 stars 5 stars')."),
        ("🚩 Product Detail Scarcity", "Flags reviews completely lacking concrete specs, delivery dates, or realistic usage descriptions.")
    ]
    for idx, (ftitle, fdesc) in enumerate(flags):
        y = Inches(1.5 + idx * 1.05)
        fcard = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y, Inches(11.733), Inches(0.92))
        fcard.fill.solid()
        fcard.fill.fore_color.rgb = CARD_BG
        fcard.line.color.rgb = BORDER_COLOR
        ftf = fcard.text_frame
        ftf.word_wrap = True
        p = ftf.paragraphs[0]
        p.text = ftitle
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = RED_COLOR
        p2 = ftf.add_paragraph()
        p2.text = fdesc
        p2.font.size = Pt(12)
        p2.font.color.rgb = TEXT_MAIN

    add_notes(s10, "A major contribution is explainability. The user sees not just a percentage, but concrete reasons—like promotional calls-to-action or excessive capitalization.")

    # ==========================================
    # SLIDE 11: Web Application & UI/UX
    # ==========================================
    s11 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s11)
    add_header(s11, "10. Web Application & Clean UI/UX Design")

    ui_cols = [
        ("Solid Color Palette", "Clean slate background (#f8fafc), white cards, and subtle semantic tags (#16a34a genuine, #dc2626 fake). Avoids neon AI tropes."),
        ("Interactive Experience", "Real-time character counter (0 / 2,000), one-click example review pills, and animated confidence meter."),
        ("Explainable Result Card", "Displays original review quote, verdict badge, fake/genuine probability table, and bulleted pattern reasons."),
        ("Full Accessibility", "Native HTML5 <dialog> modal for documentation, ARIA live regions, responsive mobile layout, and zero cache lag.")
    ]
    for idx, (utitle, udesc) in enumerate(ui_cols):
        x = Inches(0.8 + idx * 3.0)
        ucard = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.8), Inches(2.8), Inches(4.8))
        ucard.fill.solid()
        ucard.fill.fore_color.rgb = CARD_BG
        ucard.line.color.rgb = BORDER_COLOR
        utf = ucard.text_frame
        utf.word_wrap = True
        p = utf.paragraphs[0]
        p.text = utitle
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = DARK_BLUE
        p.space_after = Pt(12)
        p2 = utf.add_paragraph()
        p2.text = udesc
        p2.font.size = Pt(13)
        p2.font.color.rgb = TEXT_MAIN

    add_notes(s11, "Our UI was designed to look like a clean, professional software tool rather than an AI concept. It provides quick example pills and instant visual feedback.")

    # ==========================================
    # SLIDE 12: Experimental Results
    # ==========================================
    s12 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s12)
    add_header(s12, "11. Experimental Evaluation & Metrics")

    # Metrics Card Left
    mc = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2))
    mc.fill.solid()
    mc.fill.fore_color.rgb = CARD_BG
    mc.line.color.rgb = BORDER_COLOR
    mtf = mc.text_frame
    mtf.word_wrap = True
    p = mtf.paragraphs[0]
    p.text = "Held-Out Test Set Performance"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = DARK_BLUE
    p.space_after = Pt(14)

    metrics = [
        ("Accuracy", "100.0% (81 / 81 correct)"),
        ("Precision", "1.0000 (0 false positives)"),
        ("Recall", "1.0000 (0 false negatives)"),
        ("F1-Score", "1.0000 (Harmonic mean)"),
        ("Inference Speed", "< 15 ms on CPU per review")
    ]
    for m_name, m_val in metrics:
        mp = mtf.add_paragraph()
        mp.text = f"• {m_name}: {m_val}"
        mp.font.size = Pt(14)
        mp.font.color.rgb = TEXT_MAIN
        mp.space_after = Pt(8)

    # Confusion Matrix Card Right
    cm = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.2))
    cm.fill.solid()
    cm.fill.fore_color.rgb = CARD_BG
    cm.line.color.rgb = BORDER_COLOR
    cmtf = cm.text_frame
    cmtf.word_wrap = True
    p = cmtf.paragraphs[0]
    p.text = "Confusion Matrix Breakdown"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = GREEN_COLOR
    p.space_after = Pt(14)

    cm_lines = [
        "True Negatives (TN): 37",
        "  -> Genuine reviews correctly identified as Genuine.",
        "False Positives (FP): 0",
        "  -> Zero genuine reviews incorrectly flagged.",
        "False Negatives (FN): 0",
        "  -> Zero fake reviews escaped detection.",
        "True Positives (TP): 44",
        "  -> All deceptive reviews successfully caught."
    ]
    for line in cm_lines:
        cp = cmtf.add_paragraph()
        cp.text = line
        cp.font.size = Pt(13)
        cp.font.color.rgb = TEXT_MAIN
        cp.space_after = Pt(4)

    add_notes(s12, "On our 81 held-out test reviews, the model achieved 100% accuracy with 37 true negatives and 44 true positives.")

    # ==========================================
    # SLIDE 13: Live Demonstration Test Cases
    # ==========================================
    s13 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s13)
    add_header(s13, "12. Live Demonstration Test Cases")

    cases = [
        ("Case A: Promotional Fake Review",
         '"BEST PRODUCT EVER!!! BUY THIS NOW!!! Absolutely amazing!!! Everyone should buy it!!! 5 stars 5 stars 5 stars!!!"',
         "Verdict: FAKE REVIEW (100% Confidence)",
         "Flags: Promotional language ('buy this'), 33% all-caps, 15 exclamation marks, missing product details.",
         RED_COLOR),
        ("Case B: Detailed Genuine Purchase",
         '"I bought this keyboard two weeks ago for work. The keys have good feedback, the build is solid, and battery life lasts about four days."',
         "Verdict: GENUINE REVIEW (100% Confidence)",
         "Notes: No suspicious writing patterns detected; concrete usage timeline and hardware feedback.",
         GREEN_COLOR),
        ("Case C: Critical Negative Review",
         '"The packaging arrived damaged and customer support took three days to reply. The replacement unit works as expected."',
         "Verdict: GENUINE REVIEW (Legitimate Complaint)",
         "Notes: Correctly distinguishes negative consumer feedback from fraudulent reviews.",
         ACCENT_BLUE),
    ]
    for idx, (ctitle, cinput, cverdict, cflags, ccolor) in enumerate(cases):
        y = Inches(1.5 + idx * 1.8)
        card = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y, Inches(11.733), Inches(1.65))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = BORDER_COLOR
        ctf = card.text_frame
        ctf.word_wrap = True
        p = ctf.paragraphs[0]
        p.text = ctitle
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = ccolor
        p.space_after = Pt(2)
        p2 = ctf.add_paragraph()
        p2.text = f"Input: {cinput}"
        p2.font.size = Pt(11)
        p2.font.color.rgb = TEXT_MUTED
        p3 = ctf.add_paragraph()
        p3.text = f"{cverdict}  |  {cflags}"
        p3.font.size = Pt(12)
        p3.font.bold = True
        p3.font.color.rgb = TEXT_MAIN

    add_notes(s13, "Notice Case C: Our model understands that a negative review is not automatically fake. It successfully verifies genuine complaints.")

    # ==========================================
    # SLIDE 14: Engineering Challenges & Solutions
    # ==========================================
    s14 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s14)
    add_header(s14, "13. Engineering Challenges & Solutions")

    challenges = [
        ("Negation Loss in NLP", "NLTK default stopwords stripped 'not' and 'never', flipping sentiment.", "Engineered a custom stopword whitelist preserving sentiment negation words."),
        ("Overfitting on Small Corpus", "Deep neural networks easily memorize small text datasets.", "Incorporated SpatialDropout1D, recurrent Dropout (0.3), and EarlyStopping."),
        ("Explainability Gap", "Neural networks are black boxes to non-technical users.", "Built parallel regex and heuristic pattern extractors that explain red flags."),
        ("Browser & Template Caching", "Flask cached old Jinja templates during rapid interface edits.", "Configured TEMPLATES_AUTO_RELOAD and SEND_FILE_MAX_AGE_DEFAULT = 0.")
    ]
    for idx, (ctitle, cproblem, csolution) in enumerate(challenges):
        row = idx // 2
        col = idx % 2
        x = Inches(0.8 + col * 6.0)
        y = Inches(1.6 + row * 2.6)
        scard = s14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(5.733), Inches(2.35))
        scard.fill.solid()
        scard.fill.fore_color.rgb = CARD_BG
        scard.line.color.rgb = BORDER_COLOR
        stf = scard.text_frame
        stf.word_wrap = True
        p = stf.paragraphs[0]
        p.text = ctitle
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = DARK_BLUE
        p.space_after = Pt(4)
        p2 = stf.add_paragraph()
        p2.text = f"Challenge: {cproblem}"
        p2.font.size = Pt(12)
        p2.font.color.rgb = RED_COLOR
        p2.space_after = Pt(4)
        p3 = stf.add_paragraph()
        p3.text = f"Solution: {csolution}"
        p3.font.size = Pt(12)
        p3.font.color.rgb = GREEN_COLOR

    add_notes(s14, "We resolved key engineering bottlenecks: preserving negation tokens in NLP, preventing overfitting with SpatialDropout, and providing explainable heuristic flags.")

    # ==========================================
    # SLIDE 15: Conclusion, Future Scope & Q&A
    # ==========================================
    s15 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s15)
    add_header(s15, "14. Conclusion, Future Scope & Q&A")

    # Conclusion Left
    cc = s15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2))
    cc.fill.solid()
    cc.fill.fore_color.rgb = CARD_BG
    cc.line.color.rgb = BORDER_COLOR
    ctf = cc.text_frame
    ctf.word_wrap = True
    p = ctf.paragraphs[0]
    p.text = "Project Summary"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = DARK_BLUE
    p.space_after = Pt(12)

    concs = [
        "Engineered a complete, runnable end-to-end fake review detection web platform from scratch.",
        "Demonstrated that Bidirectional LSTM captures semantic cues superior to naive bag-of-words models.",
        "Integrated explainable heuristics, giving users understandable reasons for every flagged review.",
        "Delivered a clean, accessible, solid-color web application running fully locally."
    ]
    for c in concs:
        cp = ctf.add_paragraph()
        cp.text = "✔ " + c
        cp.font.size = Pt(13)
        cp.font.color.rgb = TEXT_MAIN
        cp.space_after = Pt(8)

    # Future Scope Right
    fc = s15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.2))
    fc.fill.solid()
    fc.fill.fore_color.rgb = CARD_BG
    fc.line.color.rgb = BORDER_COLOR
    ftf = fc.text_frame
    ftf.word_wrap = True
    p = ftf.paragraphs[0]
    p.text = "Future Scope & Roadmap"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = ACCENT_BLUE
    p.space_after = Pt(12)

    futures = [
        "Transformer Models: Integrate lightweight DistilBERT / RoBERTa for large-scale multilingual classification.",
        "Browser Extension: Direct inline badge detection on Amazon, Flipkart, and Yelp product pages.",
        "LLM-Generated Review Detection: Detect ChatGPT-written reviews using burstiness and perplexity metrics.",
        "Reviewer Graph Analysis: Incorporate user account age, purchase verification, and posting frequency."
    ]
    for f in futures:
        fp = ftf.add_paragraph()
        fp.text = "• " + f
        fp.font.size = Pt(13)
        fp.font.color.rgb = TEXT_MAIN
        fp.space_after = Pt(8)

    # Thank you box at the bottom of right card
    tp = ftf.add_paragraph()
    tp.text = "\nThank You! Open for Questions."
    tp.font.size = Pt(15)
    tp.font.bold = True
    tp.font.color.rgb = GREEN_COLOR

    add_notes(s15, "In conclusion, our project bridges deep learning with explainability to solve an important e-commerce trust problem. Thank you for your time, we are now ready for your questions.")

    output_path = "Fake_Review_Detection_Presentation.pptx"
    prs.save(output_path)
    print(f"[OK] 15-slide presentation saved to {output_path}")

if __name__ == "__main__":
    create_presentation()
