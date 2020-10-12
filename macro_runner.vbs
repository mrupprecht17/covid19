Set objExcel = CreateObject("Excel.Application")
Set objWorkbook = objExcel.Workbooks.Open("C:\Users\Michael\OneDrive - California Institute of Technology\Documents\musings, et cetera\COVID-19\COVID-19 IL data.xlsm")

objExcel.Visible = False
objExcel.Run("ReadNewestData")

objWorkbook.Save
objWorkbook.Close SaveChanges=True
objExcel.Quit

Set objWorkbook = Nothing
Set objExcel = Nothing
