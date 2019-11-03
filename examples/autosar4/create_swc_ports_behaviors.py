
import autosar
import autosar.rte
import autosar.bsw

outFolder = './project/out/'

def init_ws():
    ws = autosar.workspace(version="4.2.2")
    #Create Packages
    datatypes = ws.createPackage('DataTypes', role='DataType')
    datatypes.createSubPackage('CompuMethods', role='CompuMethod')
    datatypes.createSubPackage('DataConstrs', role='DataConstraint')    
    basetypes = datatypes.createSubPackage('BaseTypes')
    portinterfaces = ws.createPackage('PortInterfaces', role="PortInterface")
    components = ws.createPackage('ComponentTypes', role='ComponentType')
    constants = ws.createPackage('Constants', role='Constant')
    #Create DataTypes    
    basetypes.createSwBaseType('uint16', 16, nativeDeclaration='uint16')
    datatypes.createImplementationDataType('uint16', lowerLimit=0, upperLimit=65535, baseTypeRef='/DataTypes/BaseTypes/uint16', typeEmitter='Platform_Type')
    #Create Constants
    constants.createConstant('VehicleSpeed_IV', 'uint16', 65535)
    constants.createConstant('EngineSpeed_IV', 'uint16', 65535)
    #Create PortInterfaces
    portinterfaces.createSenderReceiverInterface('VehicleSpeed_I', autosar.DataElement('VehicleSpeed', 'uint16'))
    portinterfaces.createSenderReceiverInterface('EngineSpeed_I', autosar.DataElement('EngineSpeed', 'uint16'))
    return ws

componentName1 = 'SWC1'
componentName2 = 'SWC2'

def main():
    ws = init_ws()
    components = ws.find('/ComponentTypes')
    
    # COMPONENT 1
    swc1 = components.createApplicationSoftwareComponent(componentName1)
    port1 = swc1.createRequirePort('Port1', 'VehicleSpeed_I', initValueRef = 'VehicleSpeed_IV', aliveTimeout=30)
    swc1.createRequirePort('Port2', 'EngineSpeed_I', initValueRef = 'EngineSpeed_IV', aliveTimeout=30)
    runnable_swc1_init = swc1.behavior.createRunnable(componentName1+'_Init')
    runnable_swc1_exit = swc1.behavior.createRunnable(componentName1+'_Exit')
    runnable_swc1_run = swc1.behavior.createRunnable(componentName1+'_Run', portAccess=['Port1','Port2'])
    swc1.behavior.createTimerEvent(componentName1+'_Run', 20)

    # COMPONENT 2
    swc2 = components.createApplicationSoftwareComponent(componentName2)
    swc2.createProvidePort('Port1', 'VehicleSpeed_I', initValueRef = 'VehicleSpeed_IV', aliveTimeout=30)
    swc2.createProvidePort('Port2', 'EngineSpeed_I', initValueRef = 'EngineSpeed_IV', aliveTimeout=30)
    runnable_swc2_init = swc2.behavior.createRunnable(componentName2+'_Init')
    runnable_swc2_exit = swc2.behavior.createRunnable(componentName2+'_Exit')
    runnable_swc2_run = swc2.behavior.createRunnable(componentName2+'_Run', portAccess=['Port1','Port2'])
    ev_ = swc2.behavior.createTimerEvent(componentName2+'_Run', 20)

    partition = autosar.rte.Partition()
    pkg = ws.getComponentTypePackage()
    partition.addComponent(pkg[componentName1])
    partition.addComponent(pkg[componentName2])
    partition.finalize()
    rtegen = autosar.rte.TypeGenerator(partition)
    rtegen.generate(outFolder)
    rtegen = autosar.rte.ComponentHeaderGenerator(partition)
    rtegen.generate(outFolder)
    rtegen = autosar.rte.MockRteGenerator(partition)
    rtegen.generate(outFolder)
    osconfig = autosar.bsw.OsConfig(partition)
    testtask1 = osconfig.create_task("TestTask1")
    testtask1.map_runnable(partition.components[0].runnables[2])
    testtask1.map_runnable(partition.components[1].runnables[2])
    rtegen = autosar.rte.RteTaskGenerator(partition,osconfig)
    rtegen.generate(outFolder)

    bswgen = autosar.bsw.generator.OsConfigGenerator(osconfig)
    bswgen.generate(outFolder)
    

    #save SWC1 into separate ARXML file
    ws.saveXML(outFolder + '{}.arxml'.format('SWC'))

    print("Done!")

if __name__ == "__main__":
    main()