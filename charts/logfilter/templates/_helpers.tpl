{{/*
The chart name
*/}}
{{- define "ourapp.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
If release name contains chart name it will be used as a full name.
*/}}
{{- define "ourapp.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Define the chart name and version, just like the chart label.
*/}}
{{- define "ourapp.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Define some common labels
*/}}
{{- define "ourapp.labels" -}}
helm.sh/chart: {{ include "ourapp.chart" . }}
app: "ourapp"
{{ include "ourapp.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- with .Values.commonLabels }}
{{ toYaml . }}
{{- end }}
{{- end }}

{{/*
Define the selector labels
*/}}
{{- define "ourapp.selectorLabels" -}}
app.kubernetes.io/name: {{ include "ourapp.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app: "ourapp"
{{- end }}

{{/*
Defime the service account anme
*/}}
{{- define "ourapp.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "ourapp.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Define the image
*/}}
{{- define "ourapp.image" -}}
{{- printf "%s:%s" .Values.image.repository (default (printf "v%s" .Chart.AppVersion) .Values.image.tag) }}
{{- end }}
