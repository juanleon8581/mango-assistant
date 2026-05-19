## ADDED Requirements

### Requirement: Copy output to clipboard
El sistema SHALL mantener un buffer de texto plano del output de la última macro ejecutada. Cuando el usuario presiona `ctrl+c` y el output panel está visible, el sistema SHALL copiar el contenido completo del buffer al clipboard del sistema y mostrar una notificación de confirmación.

#### Scenario: Copy after successful macro
- **WHEN** una macro termina de ejecutarse y el usuario presiona `ctrl+c`
- **THEN** el sistema copia todo el output al clipboard y muestra la notificación "Copied to clipboard"

#### Scenario: Copy after failed macro
- **WHEN** una macro falla y el panel de output muestra el error, y el usuario presiona `ctrl+c`
- **THEN** el sistema copia todo el output (incluyendo el mensaje de error) al clipboard

#### Scenario: ctrl+c sin output visible
- **WHEN** el usuario presiona `ctrl+c` y el panel de output no está visible (no se ha ejecutado ninguna macro aún)
- **THEN** el evento no es interceptado y Textual ejecuta su comportamiento por defecto

### Requirement: Plain text buffer
El buffer de clipboard SHALL contener texto plano sin Rich markup tags ni ANSI escape codes. El output renderizado en pantalla (con colores) no se ve afectado.

#### Scenario: Buffer strips Rich markup
- **WHEN** el runner emite `[bold cyan][step 1/2][/] $ git fetch`
- **THEN** el buffer almacena `[step 1/2] $ git fetch`

#### Scenario: Buffer strips ANSI codes
- **WHEN** el subprocess emite output con color codes ANSI (ej. de git)
- **THEN** el buffer almacena el texto plano sin los escape codes

#### Scenario: Buffer resets on new execution
- **WHEN** el usuario ejecuta una nueva macro mientras hay output previo en el panel
- **THEN** el buffer se vacía antes de capturar el output de la nueva macro
