# Spec: command-runner

## Purpose

Define how mango executes macro steps — sequential subprocess execution, output streaming, parameter substitution, and working directory management.

## Requirements

### Requirement: Sequential step execution
El sistema SHALL ejecutar los pasos de una macro en orden secuencial. Si un paso retorna exit code distinto de 0, el sistema SHALL detener la ejecución y no correr los pasos restantes.

#### Scenario: All steps succeed
- **WHEN** una macro tiene 3 pasos y todos retornan exit code 0
- **THEN** el sistema ejecuta los 3 pasos en orden y reporta éxito

#### Scenario: Step fails mid-sequence
- **WHEN** el segundo paso de tres retorna exit code != 0
- **THEN** el sistema detiene la ejecución, no ejecuta el tercer paso, y reporta el error del segundo paso

### Requirement: Working directory
El sistema SHALL ejecutar todos los pasos en el directorio de trabajo desde el cual el usuario lanzó `mango`, sin modificar el `cwd` del proceso padre.

#### Scenario: Execution uses launch directory
- **WHEN** el usuario ejecuta `mango` desde `/home/user/projects/my-app`
- **THEN** todos los pasos de cualquier macro se ejecutan con `cwd=/home/user/projects/my-app`

### Requirement: Real-time output streaming
El sistema SHALL capturar y mostrar el stdout y stderr de cada paso en tiempo real mientras se ejecuta, sin esperar a que el paso complete.

#### Scenario: Long-running command output
- **WHEN** un paso tarda varios segundos en completar (e.g., `git fetch`)
- **THEN** el output parcial aparece en el panel de output a medida que el proceso lo genera

### Requirement: Parameter substitution before execution
El sistema SHALL reemplazar todos los placeholders `{param_name}` en cada step con los valores provistos por el usuario antes de pasar el comando al subproceso.

#### Scenario: All params substituted
- **WHEN** el step es `git checkout {branch}` y el usuario ingresó `feature/login`
- **THEN** el comando ejecutado es `git checkout feature/login`

#### Scenario: Unresolved placeholder
- **WHEN** un step contiene `{param_name}` pero no hay un parámetro con ese nombre definido en la macro
- **THEN** el sistema reporta un error de configuración antes de ejecutar cualquier paso

### Requirement: Non-interactive subprocess execution
Los pasos SHALL ejecutarse como subprocesos no interactivos. El sistema no SHALL intentar conectar el stdin del usuario al proceso hijo (mango no es un multiplexor de terminal).

#### Scenario: Command requires no stdin
- **WHEN** se ejecuta `git fetch` como paso
- **THEN** el proceso corre sin stdin conectado y el output se captura y muestra en el panel
