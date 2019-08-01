import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import autosar
from tests.arxml.common import ARXMLTestClass
import unittest

def _create_packages(ws):

    package=ws.createPackage('DataTypes', role='DataType')
    package.createSubPackage('CompuMethods', role='CompuMethod')
    package.createSubPackage('DataConstrs', role='DataConstraint')
    package.createSubPackage('Units', role='Unit')
    package.createSubPackage('BaseTypes')
    package = ws.createPackage('ModeDclrGroups', role = 'ModeDclrGroup')
    package = ws.createPackage('Constants', role='Constant')
    package = ws.createPackage('ComponentTypes', role='ComponentType')
    package = ws.createPackage('PortInterfaces', role="PortInterface")


def _create_data_types(ws):
    basetypes = ws.find('/DataTypes/BaseTypes')
    basetypes.createSwBaseType('boolean', 1, 'BOOLEAN')
    basetypes.createSwBaseType('uint8', 8, nativeDeclaration='uint8')
    basetypes.createSwBaseType('uint16', 16, nativeDeclaration='uint16')
    basetypes.createSwBaseType('uint32', 32, nativeDeclaration='uint32')
    basetypes.createSwBaseType('float32', 32, encoding='IEEE754')
    package = ws.find('DataTypes')
    package.createImplementationDataType('boolean', valueTable=['FALSE','TRUE'], baseTypeRef='/DataTypes/BaseTypes/boolean', typeEmitter='Platform_Type')
    package.createImplementationDataType('uint8', lowerLimit=0, upperLimit=255, baseTypeRef='/DataTypes/BaseTypes/uint8', typeEmitter='Platform_Type')
    package.createImplementationDataType('uint16', lowerLimit=0, upperLimit=65535, baseTypeRef='/DataTypes/BaseTypes/uint16', typeEmitter='Platform_Type')
    package.createImplementationDataType('uint32', lowerLimit=0, upperLimit=4294967295, baseTypeRef='/DataTypes/BaseTypes/uint32', typeEmitter='Platform_Type')
    package.createImplementationDataTypeRef('OffOn_T', implementationTypeRef = '/DataTypes/uint8',
                                            valueTable = ['OffOn_Off',
                                                          'OffOn_On',
                                                          'OffOn_Error',
                                                          'OffOn_NotAvailable'
                                                        ])
    package.createImplementationDataTypeRef('Seconds_T', '/DataTypes/uint8', lowerLimit=0, upperLimit=63)
    package.createImplementationDataTypeRef('Minutes_T', '/DataTypes/uint8', lowerLimit=0, upperLimit=63)
    package.createImplementationDataTypeRef('Hours_T', '/DataTypes/uint8', lowerLimit=0, upperLimit=31)
    

def _init_ws(ws):
    _create_packages(ws)
    _create_data_types(ws)

class ARXML4PortInterfaceTest(ARXMLTestClass):
    
    def test_create_sender_receiver_interface_single_element(self):
        ws = autosar.workspace(version="4.2.2")
        _init_ws(ws)
        package = ws.find('/PortInterfaces')
        itf1 =  package.createSenderReceiverInterface('HeaterPwrStat_I', autosar.element.DataElement('HeaterPwrStat', 'OffOn_T'))
        file_name = 'ar4_sender_receiver_interface_single_element.arxml'
        generated_file = os.path.join(self.output_dir, file_name)
        expected_file = os.path.join( 'expected_gen', 'portinterface', file_name)        
        self.save_and_check(ws, expected_file, generated_file)
        ws2 = autosar.workspace(version="4.2.2")
        ws2.loadXML(os.path.join(os.path.dirname(__file__), expected_file))
        itf2 = portInterface = ws2.find(itf1.ref)
        self.assertIsInstance(itf2, autosar.portinterface.SenderReceiverInterface)
        
    def test_create_sender_receiver_interface_multiple_elements_explicit(self):
        ws = autosar.workspace(version="4.2.2")
        _init_ws(ws)
        package = ws.find('/PortInterfaces')
        itf1 = package.createSenderReceiverInterface('SystemTime_I', [
            autosar.element.DataElement('Seconds', '/DataTypes/Seconds_T'),
            autosar.element.DataElement('Minutes', '/DataTypes/Minutes_T'),
            autosar.element.DataElement('Hours', '/DataTypes/Hours_T')
            ])
        file_name = 'ar4_sender_receiver_interface_multiple_elements_explicit.arxml'
        generated_file = os.path.join(self.output_dir, file_name)
        expected_file = os.path.join( 'expected_gen', 'portinterface', file_name)        
        self.save_and_check(ws, expected_file, generated_file)
        ws2 = autosar.workspace(version="4.2.2")
        ws2.loadXML(os.path.join(os.path.dirname(__file__), expected_file))
        itf2 = portInterface = ws2.find(itf1.ref)
        self.assertIsInstance(itf2, autosar.portinterface.SenderReceiverInterface)        
        
if __name__ == '__main__':
    unittest.main()