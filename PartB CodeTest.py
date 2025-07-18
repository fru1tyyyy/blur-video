import numpy as np
import cv2
import matplotlib.pyplot as plt

for i in range(1, 9):
    # Read image in grayscale
    img = cv2.imread(f"img/00{i}.png", 0)
    nrow, ncol = img.shape
    
    #Binarize image (black text = 0, white background = 255)
    _, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    
    #Horizontal projection to detect row blocks as paragraphs
    row_hist = np.sum(img == 0, axis=1)
    row_blocks = []
    in_text = False
    white_streak = 0
    
    for r in range(nrow):
        if row_hist[r] < 3:
            white_streak += 1
        else:
            if white_streak >= 15 and in_text:
                row_blocks[-1][1] = r - white_streak
                in_text = False
            white_streak = 0
            if not in_text:
                row_blocks.append([r, None])
                in_text = True
    if in_text:
        row_blocks[-1][1] = nrow - 1
        
    para_count = 0
        
    for r_start, r_end in row_blocks:
        row_img = img[r_start:r_end, :]
        col_hist = np.sum(row_img == 0, axis=0)
        col_blocks = []
        in_text = False
        white_streak = 0
    
        for c in range(ncol):
            if col_hist[c] < 20:
                white_streak += 1
            else:
                if white_streak >= 10 and in_text:
                    col_blocks[-1][1] = c - white_streak
                    in_text = False
                white_streak = 0
                if not in_text:
                    col_blocks.append([c, None])
                    in_text = True
        if in_text:
            col_blocks[-1][1] = nrow - 1
        
        for c_start, c_end in col_blocks:
            region = img[r_start:r_end, c_start:c_end]
            para_count += 1
            output_path = f"extracted_paragraphs/image_{i}_para_{para_count}.png"
            cv2.imwrite(output_path, region)

    plt.figure(figsize=(12, 4))
    plt.plot(row_hist)
    plt.title(f"Row Histogram (Black Pixel Count per Row for image {i})")
    plt.xlabel("Row Index")
    plt.ylabel("Black Pixel Count")
    plt.grid(True)
    plt.show()
        
 # Contour check to skip images/diagrams
 region_inv = cv2.bitwise_not(region.astype(np.uint8))
 contours, _ = cv2.findContours(region_inv, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
 num_contours = len(contours)
 avg_area = np.mean([cv2.contourArea(cnt) for cnt in contours]) if contours else 0
 if black_ratio > 0.4 or (num_contours < 10 and avg_area > 500):
     continue

        