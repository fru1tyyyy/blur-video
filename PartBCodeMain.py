import numpy as np
import cv2

for i in range(1, 9):
    # Read and use image in grayscale
    img = cv2.imread(f"img/00{i}.png", 0)
    nrow, ncol = img.shape
    
    #Binarize image *(black text = 0, white background = 255)
    _, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    
    #Vertical projection to detect column blocks with appropriate black pixels
    col_hist = np.sum(img == 0, axis=0)
    col_blocks = []
    in_text = False
    white_streak = 0
    
    for c in range(ncol):
        if col_hist[c] < 30:
            white_streak += 1
        else:
            if white_streak >= 15 and in_text and (c - col_blocks[-1][0]) > 100:
                col_blocks[-1][1] = c - white_streak
                in_text = False
            white_streak = 0
            if not in_text:
                col_blocks.append([c, None])
                in_text = True
    if in_text:
        col_blocks[-1][1] = ncol - 1
    
    para_count = 0
    
    #For each column block, find row blocks (paragraphs)
    for c_start, c_end in col_blocks:
        col_img = img[:, c_start:c_end]
        row_hist = np.sum(col_img == 0, axis=1)
        row_blocks = []
        in_text = False
        white_streak = 0
    
        for r in range(nrow):
            if row_hist[r] < 5:
                white_streak += 1
            else:
                if white_streak >= 30 and in_text and (r - row_blocks[-1][0]) > 40:
                    row_blocks[-1][1] = r - white_streak
                    in_text = False
                white_streak = 0
                if not in_text:
                    row_blocks.append([r, None])
                    in_text = True
        if in_text:
            row_blocks[-1][1] = nrow - 1
    
        #Trim and save each paragraph region
        for r_start, r_end in row_blocks:
            region = img[r_start:r_end, c_start:c_end]
    
            # Trim top and bottom
            row_hist_trim = np.sum(region == 0, axis=1)
            top = 0
            bottom = region.shape[0] - 1
            for r in range(region.shape[0]):
                if row_hist_trim[r] > 5:
                    top = max(0, r - 1)
                    break
            for r in range(region.shape[0] - 1, -1, -1):
                if row_hist_trim[r] > 5:
                    bottom = min(region.shape[0] - 1, r + 1)
                    break
            region = region[top:bottom + 1, :]
    
            # Trim left and right
            col_hist_trim = np.sum(region == 0, axis=0)
            left = 0
            right = region.shape[1] - 1
            for c in range(region.shape[1]):
                if col_hist_trim[c] > 10:
                    left = max(0, c - 2)
                    break
            for c in range(region.shape[1] - 1, -1, -1):
                if col_hist_trim[c] > 10:
                    right = min(region.shape[1] - 1, c + 2)
                    break
            region = region[:, left:right + 1]
    
            #Filter by size and black pixel ratio
            if region.shape[0] < 10 or region.shape[1] < 30:
                continue
            black_ratio = np.sum(region == 0) / region.size
            if black_ratio < 0.1 or black_ratio > 0.5:
                continue
            
            para_count += 1
            output_path = f"extracted_paragraphs/image_{i}_para_{para_count}.png"
            cv2.imwrite(output_path, region)
