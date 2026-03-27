# 3D Location Model for XdAnyType

- **Proposed by**: Tim Cook, 2026-03-27
- **Status**: PROPOSED

## Summary

Replace the current 2D point (latitude/longitude) location model in XdAnyType with a 3D-capable location model that supports Earth surface, Earth altitude, and solar system coordinates through a required reference frame attribute.

## Motivation

The current SDC4 location model is a simple 2D point (latitude, longitude) using WGS84. This is insufficient for:

- **Altitude-dependent data**: Aviation, mountaineering, subsurface mining, oceanography -- where the Z axis carries critical meaning
- **Space applications**: Satellite telemetry, planetary science, orbital mechanics -- where coordinates require a different reference frame entirely
- **Indoor/subsurface positioning**: Building floor, mine level, submarine depth -- where altitude/depth relative to surface matters

A 2D point on the Earth's surface was adequate for SDC4's initial scope but is a known limitation.

## Proposed Design

### Base Types (Reference Model level -- uses extension)

**Point2D**: Longitude + latitude (backward compatible with SDC4)

**Point3D**: Extends Point2D with a distance/altitude element

**Location**: Extends Point3D with a required reference frame and an optional epoch

### Reference Frames

| Frame | Description | Use Case |
|-------|-------------|----------|
| WGS84 | Earth GPS (distance = altitude in meters above ellipsoid) | Terrestrial |
| ICRF | International Celestial Reference Frame | Solar system, satellites |
| Heliocentric | Sun-centered ecliptic coordinates | Planetary science |

The frame enumeration is extensible for future needs (selenocentric, areocentric, etc.) via the standard SDC restriction mechanism in data models.

### Epoch

Optional `xs:dateTime` attribute. For Earth-surface applications, epoch is unnecessary (coordinates are stable). For space applications, epoch is critical -- orbital positions are meaningless without a time reference.

### XSD Sketch (idea starter, not final)

```xml
<xs:complexType name="Point2D">
    <xs:sequence>
        <xs:element name="longitude" type="xs:decimal"/>
        <xs:element name="latitude" type="xs:decimal"/>
    </xs:sequence>
</xs:complexType>

<xs:complexType name="Point3D">
    <xs:complexContent>
        <xs:extension base="Point2D">
            <xs:sequence>
                <xs:element name="distance" type="xs:decimal"/>
            </xs:sequence>
            <xs:attribute name="unit" type="xs:string" use="required"/>
        </xs:extension>
    </xs:complexContent>
</xs:complexType>

<xs:complexType name="LocationType">
    <xs:complexContent>
        <xs:extension base="Point3D">
            <xs:attribute name="frame" use="required">
                <xs:simpleType>
                    <xs:restriction base="xs:string">
                        <xs:enumeration value="WGS84"/>
                        <xs:enumeration value="ICRF"/>
                        <xs:enumeration value="Heliocentric"/>
                    </xs:restriction>
                </xs:simpleType>
            </xs:attribute>
            <xs:attribute name="epoch" type="xs:dateTime"/>
        </xs:extension>
    </xs:complexContent>
</xs:complexType>
```

Note: This is an idea starter. The final design needs review against the full XdAnyType hierarchy and SDC naming conventions.

## Open Design Questions

- Should the unit attribute use a restricted enumeration (meters, feet, AU, km) or follow the XdQuantity units pattern with ontology links?
- Should Point2D remain as a separate type for backward compatibility, or should Point3D with an optional distance element cover both cases?
- How does the distance element interact with the reference frame? For WGS84, distance is altitude above the ellipsoid. For ICRF/Heliocentric, it's radial distance. The semantics shift by frame -- should this be documented or enforced?
- Should additional reference frames be part of the RM enumeration or added via restriction in data models?
- Does the current 2D model need a migration path, or is the 2D case simply a Point3D with distance omitted/zero?

## Impact on RM

Moderate. Changes the location model in XdAnyType from a 2D point to a 3D-capable type hierarchy. Affects:

- XdAnyType definition (location fields)
- XSD generation in SDCStudio
- XML/JSON instance generation
- SHACL shapes for location validation

## Domain Neutrality Check

Yes. Geographic/spatial coordinates are domain-neutral infrastructure. Every domain has location-tagged data. The reference frame enumeration covers terrestrial and space applications without domain-specific semantics.

## Compatibility

SDC4 2D coordinates (latitude, longitude) are a subset of the proposed 3D model. Migration path: existing SDC4 location data maps to Point2D or Point3D with distance=0 and frame=WGS84.
