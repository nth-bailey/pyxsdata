# Architecture

The [ResourceTransformer][pyxsdata.codegen.transformer.ResourceTransformer] is the
orchestrator of the code generation procedure.

```mermaid
graph LR
    A[Load Resources] --> B(Parse transfer objects)
    B --> C[Convert to classes]
    C --> D[Analyze classes]
    D--> E[Write Output]
```

## Load Resource

The code generator accepts URIs indicating either local or remote file locations.

The resource type (xsd, wsdl, dtd, xml, json) is identified based on the file extension,
if present. If the resource lacks an extension, the loader will attempt to locate
specific syntax markings associated with the resource type.

If a resource cannot be accessed, a warning is issued, and the program continues its
normal flow. In the case of circular imports, resources are loaded only once.

## Parse transfer objects

A resource-specific parser is utilized to bind document information to transfer objects.
Additionally, the parsers are responsible for assigning common values required for later
analysis, such as locations, a namespace prefix-URI map, and common namespaces like xsi
and xlink.

- XSD: [SchemaParser][pyxsdata.codegen.parsers.SchemaParser]
- DTD: [DtdParser][pyxsdata.codegen.parsers.DtdParser]
- WSDL: [DefinitionsParser][pyxsdata.codegen.parsers.DefinitionsParser]
- XML: [TreeParser][pyxsdata.formats.dataclass.parsers.TreeParser]
- JSON: [json.loads][]

## Convert to classes

A resource-specific parser is utilized to convert the transfer objects to codegen
classes. These mappers encapsulate the pertinent logic detailing how the resource types
should be interpreted.

- XSD: [SchemaMapper][pyxsdata.codegen.mappers.SchemaMapper]
- DTD: [DtdMapper][pyxsdata.codegen.mappers.DtdMapper]
- WSDL: [DefinitionsMapper][pyxsdata.codegen.mappers.DefinitionsMapper]
- XML: [ElementMapper][pyxsdata.codegen.mappers.ElementMapper]
- JSON: [DictMapper][pyxsdata.codegen.mappers.DictMapper]

## Analyze classes

```mermaid
graph LR
    A[Validate classes] --> B(Process classes)
    B --> C[Validate class references]
```

### Validate Classes

- Remove types with unknown references

```xml
<xs:element name="root" ref="xs:missingOrUnknown"/>
```

- Remove duplicate types: Keep the last definition

```xml
<xs:element name="root" ref="RootType"/>
<xs:element name="root" ref="RootType"/>
```

- Remove duplicate overridden types:

```xml
<xs:override schemaLocation="over005a.xsd">
    <xs:attribute name="code" type="xs:date"/>
</xs:override>
```

- Merge redefined types:

```xml
<xs:redefine schemaLocation="schZ006.xsd">
    <xs:group name="GCustomDimProps">
        <xs:sequence>
            <xs:element name="DisplayInfo"	type="xs:unsignedInt"/>
        </xs:sequence>
    </xs:group>
</xs:redefine>
```

API: [pyxsdata.codegen.validator.ClassValidator][]

### Analyze Classes

The classes are wrapped in a [ClassContainer][pyxsdata.codegen.container.ClassContainer]
instance. It includes some easy finder methods and orchestrates flattening/filtering
processes.

The process is divided into multiple steps and handlers per step. All classes have to
pass through each step before next one starts. The order of the steps is very important!

### Step: Ungroup

- [FlattenAttributeGroups][pyxsdata.codegen.handlers.FlattenAttributeGroups]

### Step: Flatten

- [CalculateAttributePaths][pyxsdata.codegen.handlers.CalculateAttributePaths]
- [FlattenClassExtensions][pyxsdata.codegen.handlers.FlattenClassExtensions]
- [SanitizeEnumerationClass][pyxsdata.codegen.handlers.SanitizeEnumerationClass]
- [UpdateAttributesEffectiveChoice][pyxsdata.codegen.handlers.UpdateAttributesEffectiveChoice]
- [UnnestInnerClasses][pyxsdata.codegen.handlers.UnnestInnerClasses]
- [AddAttributeSubstitutions][pyxsdata.codegen.handlers.AddAttributeSubstitutions]
- [ProcessAttributeTypes][pyxsdata.codegen.handlers.ProcessAttributeTypes]
- [MergeAttributes][pyxsdata.codegen.handlers.MergeAttributes]
- [ProcessMixedContentClass][pyxsdata.codegen.handlers.ProcessMixedContentClass]

### Step: Filer

- [FilterClasses][pyxsdata.codegen.handlers.FilterClasses]

### Step: Sanitize

- [ResetAttributeSequences][pyxsdata.codegen.handlers.ResetAttributeSequences]
- [RenameDuplicateAttributes][pyxsdata.codegen.handlers.RenameDuplicateAttributes]

### Step: Resolve

- [ValidateAttributesOverrides][pyxsdata.codegen.handlers.ValidateAttributesOverrides]

### Step: Vacuum

- [VacuumInnerClasses][pyxsdata.codegen.handlers.VacuumInnerClasses]

### Step: Finalize

- [DetectCircularReferences][pyxsdata.codegen.handlers.DetectCircularReferences]
- [CreateCompoundFields][pyxsdata.codegen.handlers.CreateCompoundFields]
- [CreateWrapperFields][pyxsdata.codegen.handlers.CreateWrapperFields]
- [DisambiguateChoices][pyxsdata.codegen.handlers.DisambiguateChoices]
- [SanitizeAttributesDefaultValue][pyxsdata.codegen.handlers.SanitizeAttributesDefaultValue]
- [ResetAttributeSequenceNumbers][pyxsdata.codegen.handlers.ResetAttributeSequenceNumbers]

### Step: Designate

- [RenameDuplicateClasses][pyxsdata.codegen.handlers.RenameDuplicateClasses]
- [ValidateReferences][pyxsdata.codegen.handlers.ValidateReferences]
- [DesignateClassPackages][pyxsdata.codegen.handlers.DesignateClassPackages]
