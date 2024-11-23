from typing import Dict, List, Optional
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

class HbbTVXMLGenerator:
    """Generator for HbbTV test harness XML files"""
    
    def __init__(self):
        self.xml_namespace = "http://www.hbbtv.org/2012/testImplementation"
    
    def prettify_xml(self, elem: ET.Element) -> str:
        """Return a pretty-printed XML string"""
        rough_string = ET.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")
    
    def generate_implementation_xml(self,
                                  test_id: str,
                                  playout_set_file: str = "playoutset.xml",
                                  https_server: bool = False) -> str:
        """
        Generate implementation.xml for a test case
        
        Args:
            test_id: Test case identifier
            playout_set_file: Name of the playout set XML file
            https_server: Whether the test requires HTTPS server
            
        Returns:
            Pretty-printed XML string
        """
        # Create root element with namespace
        root = ET.Element("testImplementation", {
            "id": test_id,
            "xmlns": self.xml_namespace
        })
        
        # Add playout sets section
        playout_sets = ET.SubElement(root, "playoutSets")
        playout_set = ET.SubElement(playout_sets, "playoutSet", {
            "id": "1",
            "definition": playout_set_file
        })
        
        # Add HTTPS server config if needed
        if https_server:
            ET.SubElement(root, "httpsServerConfig")
        
        return self.prettify_xml(root)
    
    def generate_ait_xml(self,
                        test_id: str,
                        application_name: str,
                        initial_path: str = "index.html",
                        org_id: int = 0,
                        app_id: int = 1) -> str:
        """
        Generate AIT (Application Information Table) XML
        
        Args:
            test_id: Test case identifier
            application_name: Name of the application
            initial_path: Initial path to launch
            org_id: Organization ID (default 0 will be replaced by test harness)
            app_id: Application ID
            
        Returns:
            Pretty-printed XML string
        """
        root = ET.Element("ait")
        
        application = ET.SubElement(root, "application")
        ET.SubElement(application, "orgId").text = str(org_id)
        ET.SubElement(application, "appId").text = str(app_id)
        ET.SubElement(application, "controlCode").text = "AUTOSTART"
        ET.SubElement(application, "visibility").text = "VISIBLE_ALL"
        ET.SubElement(application, "serviceBound").text = "false"
        ET.SubElement(application, "priority").text = "1"
        ET.SubElement(application, "version").text = "1"
        
        profiles = ET.SubElement(application, "profiles")
        ET.SubElement(profiles, "profile").text = "0x0000"
        
        transport = ET.SubElement(application, "transport")
        http = ET.SubElement(transport, "http")
        ET.SubElement(http, "url").text = initial_path
        
        ET.SubElement(application, "applicationName").text = application_name
        
        return self.prettify_xml(root)
    
    def generate_playoutset_xml(self,
                               test_id: str,
                               service_name: str = "Test Service",
                               transport_stream_id: int = 1,
                               original_network_id: int = 1,
                               service_id: int = 1) -> str:
        """
        Generate playoutset.xml for a test case
        
        Args:
            test_id: Test case identifier
            service_name: Name of the service
            transport_stream_id: Transport stream ID
            original_network_id: Original network ID
            service_id: Service ID
            
        Returns:
            Pretty-printed XML string
        """
        root = ET.Element("playoutSet")
        
        # Add transport stream info
        ts = ET.SubElement(root, "transportStream")
        ET.SubElement(ts, "tsId").text = str(transport_stream_id)
        ET.SubElement(ts, "onId").text = str(original_network_id)
        
        # Add service info
        service = ET.SubElement(ts, "service")
        ET.SubElement(service, "serviceId").text = str(service_id)
        ET.SubElement(service, "serviceName").text = service_name
        ET.SubElement(service, "defaultAIT", {
            "type": "application/vnd.dvb.ait+xml",
            "url": "ait.xml"
        })
        
        return self.prettify_xml(root)
    
    def generate_test_xml_files(self,
                               test_id: str,
                               test_name: str,
                               output_dir: str,
                               https_required: bool = False) -> Dict[str, str]:
        """
        Generate all required XML files for a HbbTV test case
        
        Args:
            test_id: Test case identifier
            test_name: Human-readable test name
            output_dir: Directory to save the XML files
            https_required: Whether the test requires HTTPS server
            
        Returns:
            Dictionary mapping file names to their contents
        """
        xml_files = {
            "implementation.xml": self.generate_implementation_xml(
                test_id,
                https_server=https_required
            ),
            "ait.xml": self.generate_ait_xml(
                test_id,
                test_name
            ),
            "playoutset.xml": self.generate_playoutset_xml(
                test_id,
                f"Test Service - {test_name}"
            )
        }
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Write files
        for filename, content in xml_files.items():
            file_path = os.path.join(output_dir, filename)
            with open(file_path, 'w') as f:
                f.write(content)
        
        return xml_files