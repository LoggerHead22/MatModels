(defparameter *width* 104)
(defparameter *height* 32)
(defparameter *aspect* (/ *width* *height*))
(defparameter *pixel-aspect* (/ 9 20))
(defparameter *lightmap* " .:!/r(l1Z4H9W8$@")
(defparameter *n-lightmap* (length *lightmap*))
(defparameter *camera-position* #(-3 0 0))
(defparameter *light* (vector -1 0 0))
(defparameter *output* (make-string (* *width* *height*) :initial-element #\.))

(defun clamp (value low high)
    (max (min value high) low))

(defun make-vec (&rest as)
    (apply #'concatenate 'vector
        (mapcar (lambda (x) (if (typep x 'sequence) x (list x))) as)))

(defmacro vx (a)
    `(aref ,a 0))

(defun v+ (a b)
    (map 'vector #'+ a b))

(defun v* (a b)
    (map 'vector (lambda (x) (* x b)) a))

(defun v/ (a b)
    (map 'vector (lambda (x) (/ x b)) a))

(defun v. (a b)
    (reduce #'+ (map 'vector #'* a b)))

(defun v# (a)
    (sqrt (v. a a)))

(defun v#2 (a)
    (v. a a))

(defun v! (a)
    (v/ a (v# a)))

(defun sphere (o d r)
    (let* ((a (v. o d))
           (b (- (v#2 o) (* r r)))
           (h (- (* a a) b)))
        (if (< h 0)
            nil
            (let ((c (sqrt h)))
                (vector (- 0 a c) (- c b))))))

(loop for _ from 0 to 100000 do
    (loop for i from 0 to (1- *height*) do
        (loop for j from 0 to (1- *width*) do
            (let* ((x (* (1- (* (/ j *width*) 2)) *aspect* *pixel-aspect*))
                   (y (1- (* (/ i *height*) 2)))
                   (o #\.)
                   (uv (vector x y))
                   (d (v! (make-vec 1 uv))))

                (setf *light* (v! (vector (sin (* _ -0.1)) (cos (* _ 0.1)) (sin (1- (* _ 0.07))))))

                (let ((hit (sphere *camera-position* d 1)))
                    (when hit
                        (let ((brightness (v. (v! (v+ *camera-position* (v* d (vx hit)))) *light*)))
                            (setf o (aref *lightmap* (round (* (clamp brightness 0 1) (1- *n-lightmap*))))))))

                (setf (char *output* (+ (* i *width*) j)) o))))
    (format t "~a~%" *output*)
    (sleep 1e-4))