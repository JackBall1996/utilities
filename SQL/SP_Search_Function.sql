-- SP Search Function -- 
USE master;
GO


DECLARE @vcSQL VARCHAR(MAX) = '',
		@DatabaseName VARCHAR(MAX);

DECLARE C CURSOR
	FOR SELECT [Name] FROM sys.databases	
			WHERE [Name] IN ('Database Names')

OPEN C

FETCH NEXT FROM C INTO @DatabaseName;

WHILE @@FETCH_STATUS = 0

BEGIN

SET @vcSQL = '

	USE ' + @DatabaseName + ';
	
	SELECT 
		''' + @DatabaseName + ''' AS [Database],
		S.[Name] AS [Schema_Name],
		O.[Name] AS [Object_Name],
		O.[Type],
		SM.[Definition] 
		FROM sys.sql_modules AS SM
		LEFT JOIN sys.objects AS O
			ON SM.object_id = O.object_id
		LEFT JOIN sys.schemas AS S
			ON O.schema_id = S.schema_id
		WHERE SM.[Definition] LIKE ''%Search Here%''
'

EXEC(@vcSQL)


FETCH NEXT FROM C INTO @DatabaseName;

END

CLOSE C
DEALLOCATE C
