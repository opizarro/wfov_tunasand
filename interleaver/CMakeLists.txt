PROJECT(japan_parsers)

ADD_EXECUTABLE(raw_interleave raw_interleave.cpp)

TARGET_LINK_LIBRARIES(raw_interleave adt)

INCLUDE_DIRECTORIES(/usr/local/include/libadt)
