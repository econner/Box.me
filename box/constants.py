TEMP_PT_FILES_DIR = 'box/suggestion_engine/temp_pt_files/'
TEMP_PT_FILES_INFO_FILE = 'box/suggestion_engine/temp_pt_files/_file_info.txt'
SIM_INDEX_THRESHOLD = 0.8

# Poi Integration
JAVA_DEPENDENCIES_DIR = 'suggestion_engine/java_dependencies/'
POI_JARS_DIR = JAVA_DEPENDENCIES_DIR + 'poi_jars/'
JPYPE_CLASSPATH_DELIMITER = ':'
JAVA_CLASSPATH = JPYPE_CLASSPATH_DELIMITER.join([  \
                    POI_JARS_DIR + 'poi-3.7-20101029.jar', \
                    POI_JARS_DIR + 'poi-examples-3.7-20101029.jar', \
                    POI_JARS_DIR + 'poi-ooxml-3.7-20101029.jar', \
                    POI_JARS_DIR + 'poi-ooxml-schemas-3.7-20101029.jar', \
                    POI_JARS_DIR + 'poi-scratchpad-3.7-20101029.jar', \
                    POI_JARS_DIR + 'ooxml-lib/dom4j-1.6.1.jar', \
                    POI_JARS_DIR + 'ooxml-lib/geronimo-stax-api_1.0_spec-1.0.jar', \
                    POI_JARS_DIR + 'ooxml-lib/xmlbeans-2.3.0.jar', \
                    JAVA_DEPENDENCIES_DIR])