# Roadmap: futuras funcionalidades y despliegue

Este documento propone mejoras que podríamos implementar con más tiempo y recursos. Se centra en dos áreas: (1) gamificación para incrementar la motivación del estudiantado y (2) un plan técnico de despliegue en la nube (Azure, AWS o Google Cloud) alineado con la arquitectura actual del proyecto.

## Gamificación: por qué y cómo

La gamificación introduce mecánicas de juego en contextos de aprendizaje con el objetivo de aumentar motivación, constancia y disfrute. Estas mecánicas pueden convertir entregas y retroalimentación en ciclos atractivos de práctica y mejora.

### Beneficios esperados

- Incremento de la motivación intrínseca mediante metas claras y feedback inmediato.
- Mayor constancia gracias a rachas, misiones y recompensas progresivas.
- Aprendizaje más efectivo: repetición espaciada, micro-retos y feedback accionable.
- Desarrollo de habilidades metacognitivas (autoevaluación, planificación, revisión).

### Aplicación específica al evaluador de PDFs

- Puntuación de calidad por criterio (claridad, coherencia, citas, estructura, originalidad) con barra de progreso y feedback accionable.
- Buenas prácticas de integridad académica gamificadas: recompensas por citas correctas, por revisiones de similitud transparentes y por documentación de fuentes.

### Consideraciones técnicas para gamificación

- Modelado de datos: Users, Classes, Badges.
- Prevención de fraude: detección de plagio con IA, validación de citas en los documentos.
- Auditoría y privacidad: trazabilidad de cambios, borrado bajo solicitud.
