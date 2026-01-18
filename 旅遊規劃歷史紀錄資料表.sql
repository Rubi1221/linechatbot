USE [IoTDB]
GO

/****** Object:  Table [dbo].[ItineraryRecord]    Script Date: 2024/2/26 ¤W¤È 01:17:43 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[ItineraryRecord](
	[Number] [int] IDENTITY(1,1) NOT NULL,
	[UserID] [varchar](50) NOT NULL,
	[UserRecord] [nvarchar](50) NOT NULL,
	[ContentRecord] [nvarchar](max) NOT NULL,
	[CreateDate] [datetime] NULL,
 CONSTRAINT [PK_ItineraryRecord] PRIMARY KEY CLUSTERED 
(
	[Number] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

ALTER TABLE [dbo].[ItineraryRecord] ADD  CONSTRAINT [DF_ItineraryRecord_ContentRecord]  DEFAULT (getdate()) FOR [ContentRecord]
GO

ALTER TABLE [dbo].[ItineraryRecord] ADD  CONSTRAINT [DF_ItineraryRecord_CreateDate]  DEFAULT (getdate()) FOR [CreateDate]
GO


