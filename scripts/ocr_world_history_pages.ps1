# Local Windows OCR locator only. Root must point to the PRIVATE render cache.
# Never commit outputs or treat these candidate lines as scientific approval.
param([string]$Root)
$ErrorActionPreference = 'Stop'
$privateRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../.local/'))
$resolvedRoot = [IO.Path]::GetFullPath($Root)
if (-not $resolvedRoot.StartsWith($privateRoot, [StringComparison]::OrdinalIgnoreCase)) {
    throw 'OCR outputs must remain in the ignored private .local directory.'
}
Add-Type -AssemblyName System.Runtime.WindowsRuntime
[Windows.Storage.StorageFile, Windows.Storage, ContentType=WindowsRuntime] | Out-Null
[Windows.Graphics.Imaging.BitmapDecoder, Windows.Graphics.Imaging, ContentType=WindowsRuntime] | Out-Null
[Windows.Media.Ocr.OcrEngine, Windows.Foundation, ContentType=WindowsRuntime] | Out-Null
[Windows.Globalization.Language, Windows.Globalization, ContentType=WindowsRuntime] | Out-Null
$asTask = [System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object { $_.Name -eq 'AsTask' -and $_.IsGenericMethod -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' } | Select-Object -First 1
function AwaitResult($Operation, $Type) {
    $task = $asTask.MakeGenericMethod($Type).Invoke($null, @($Operation))
    $task.Wait()
    $task.Result
}
$engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromLanguage([Windows.Globalization.Language]::new('en-US'))
foreach ($img in (Get-ChildItem -LiteralPath $Root -Recurse -Filter 'pdf-*.png')) {
    $destination = [IO.Path]::ChangeExtension($img.FullName, '.lines.json')
    if (Test-Path -LiteralPath $destination) { continue }
    $file = AwaitResult ([Windows.Storage.StorageFile]::GetFileFromPathAsync($img.FullName)) ([Windows.Storage.StorageFile])
    $stream = AwaitResult ($file.OpenAsync([Windows.Storage.FileAccessMode]::Read)) ([Windows.Storage.Streams.IRandomAccessStream])
    $decoder = AwaitResult ([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)) ([Windows.Graphics.Imaging.BitmapDecoder])
    $bitmap = AwaitResult ($decoder.GetSoftwareBitmapAsync()) ([Windows.Graphics.Imaging.SoftwareBitmap])
    $recognized = AwaitResult ($engine.RecognizeAsync($bitmap)) ([Windows.Media.Ocr.OcrResult])
    $lines = @($recognized.Lines | ForEach-Object {
        $rects=@($_.Words | ForEach-Object { $_.BoundingRect })
        [ordered]@{ text=$_.Text; top=($rects.Y|Measure-Object -Minimum).Minimum; bottom=(@($rects|ForEach-Object {$_.Y+$_.Height})|Measure-Object -Maximum).Maximum }
    })
    [IO.File]::WriteAllText($destination, (ConvertTo-Json -InputObject $lines -Depth 4), [Text.UTF8Encoding]::new($false))
    $bitmap.Dispose()
    $stream.Dispose()
}
