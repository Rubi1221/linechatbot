USE [IoTDB]
GO

/****** Object:  Table [dbo].[Attractions]    Script Date: 2024/2/26 ¤W¤È 01:16:31 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Attractions](
	[CityId] [nvarchar](20) NOT NULL,
	[City] [nvarchar](10) NOT NULL,
	[AttractionsId] [nvarchar](20) NOT NULL,
	[Attactions] [nvarchar](100) NOT NULL,
	[Address] [nvarchar](100) NOT NULL,
	[BusinessHours] [nvarchar](200) NULL,
	[Telephone] [nvarchar](20) NULL,
	[TicketPrice] [nvarchar](100) NULL,
	[Web] [nvarchar](200) NULL,
	[CreateDate] [datetime] NULL,
 CONSTRAINT [PK_Attractions] PRIMARY KEY CLUSTERED 
(
	[AttractionsId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[Attractions] ADD  CONSTRAINT [DF_Attractions_CreateDate]  DEFAULT (getdate()) FOR [CreateDate]
GO


