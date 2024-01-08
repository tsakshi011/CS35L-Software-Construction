(defun gps-line ()
  "Print the current buffer line number and narrowed line number of point."
  (interactive)
  (let ((start (point-min))
        (n (line-number-at-pos)))
    (if (= start 1)
        (message "Line %d/%d" n (-(count-matches "\n" (point-min) (point-max))1)
))))
