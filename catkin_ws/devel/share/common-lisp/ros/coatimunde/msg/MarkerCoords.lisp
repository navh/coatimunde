; Auto-generated. Do not edit!


(cl:in-package coatimunde-msg)


;//! \htmlinclude MarkerCoords.msg.html

(cl:defclass <MarkerCoords> (roslisp-msg-protocol:ros-message)
  ((x
    :reader x
    :initarg :x
    :type cl:integer
    :initform 0)
   (y
    :reader y
    :initarg :y
    :type cl:integer
    :initform 0)
   (id
    :reader id
    :initarg :id
    :type cl:integer
    :initform 0))
)

(cl:defclass MarkerCoords (<MarkerCoords>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <MarkerCoords>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'MarkerCoords)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name coatimunde-msg:<MarkerCoords> is deprecated: use coatimunde-msg:MarkerCoords instead.")))

(cl:ensure-generic-function 'x-val :lambda-list '(m))
(cl:defmethod x-val ((m <MarkerCoords>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader coatimunde-msg:x-val is deprecated.  Use coatimunde-msg:x instead.")
  (x m))

(cl:ensure-generic-function 'y-val :lambda-list '(m))
(cl:defmethod y-val ((m <MarkerCoords>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader coatimunde-msg:y-val is deprecated.  Use coatimunde-msg:y instead.")
  (y m))

(cl:ensure-generic-function 'id-val :lambda-list '(m))
(cl:defmethod id-val ((m <MarkerCoords>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader coatimunde-msg:id-val is deprecated.  Use coatimunde-msg:id instead.")
  (id m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <MarkerCoords>) ostream)
  "Serializes a message object of type '<MarkerCoords>"
  (cl:let* ((signed (cl:slot-value msg 'x)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'y)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'id)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <MarkerCoords>) istream)
  "Deserializes a message object of type '<MarkerCoords>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'x) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'y) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'id) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<MarkerCoords>)))
  "Returns string type for a message object of type '<MarkerCoords>"
  "coatimunde/MarkerCoords")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'MarkerCoords)))
  "Returns string type for a message object of type 'MarkerCoords"
  "coatimunde/MarkerCoords")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<MarkerCoords>)))
  "Returns md5sum for a message object of type '<MarkerCoords>"
  "ca2ee5708d6b15e6c81bdddf36bf281e")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'MarkerCoords)))
  "Returns md5sum for a message object of type 'MarkerCoords"
  "ca2ee5708d6b15e6c81bdddf36bf281e")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<MarkerCoords>)))
  "Returns full string definition for message of type '<MarkerCoords>"
  (cl:format cl:nil "int32 x~%int32 y~%int32 id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'MarkerCoords)))
  "Returns full string definition for message of type 'MarkerCoords"
  (cl:format cl:nil "int32 x~%int32 y~%int32 id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <MarkerCoords>))
  (cl:+ 0
     4
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <MarkerCoords>))
  "Converts a ROS message object to a list"
  (cl:list 'MarkerCoords
    (cl:cons ':x (x msg))
    (cl:cons ':y (y msg))
    (cl:cons ':id (id msg))
))
