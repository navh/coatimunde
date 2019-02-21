
(cl:in-package :asdf)

(defsystem "coatimunde-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "PointCoords" :depends-on ("_package_PointCoords"))
    (:file "_package_PointCoords" :depends-on ("_package"))
    (:file "MarkerCoords" :depends-on ("_package_MarkerCoords"))
    (:file "_package_MarkerCoords" :depends-on ("_package"))
  ))