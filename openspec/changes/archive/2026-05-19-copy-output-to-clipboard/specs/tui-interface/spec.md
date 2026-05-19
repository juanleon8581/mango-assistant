## MODIFIED Requirements

### Requirement: Output panel
Durante la ejecución de una macro, el TUI SHALL mostrar un panel de output con el resultado en tiempo real de cada paso. Al finalizar todos los pasos, el panel SHALL mostrar un resumen de éxito o el error del paso fallido. Mientras el panel de output esté visible, el usuario SHALL poder copiar su contenido completo al clipboard presionando `ctrl+c`, recibiendo una notificación de confirmación.

#### Scenario: Successful execution output
- **WHEN** todos los pasos de una macro completan con exit code 0
- **THEN** el panel de output muestra el stdout/stderr de cada paso y un mensaje de éxito al final

#### Scenario: Failed step output
- **WHEN** un paso retorna exit code != 0
- **THEN** el panel de output muestra la salida del paso fallido, un mensaje de error, y la ejecución se detiene

#### Scenario: Copy output with ctrl+c
- **WHEN** el panel de output está visible y el usuario presiona `ctrl+c`
- **THEN** el sistema copia el contenido completo del output al clipboard y muestra la notificación "Copied to clipboard"
