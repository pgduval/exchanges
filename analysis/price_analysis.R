library(RSQLite)
library(ggplot2)
library(dplyr)
library(reshape)
library(ggplot2)
library(grid)

DB_DATE = '27_Sep_2016'
setwd(paste('/home/elmaster/scraper/bitcoin/exchanges/db', DB_DATE, sep="/"))

con = dbConnect(drv=SQLite(), 
                dbname="./data.db")

query = function(q) {
    return(dbGetQuery(con, q))    
}

add_credits = function() {
  grid.text("pgduval",
            x = 0.99,
            y = 0.02,
            just = "right",
            gp = gpar(fontsize = 12, col = "#777777"))
}

title_with_subtitle = function(title, subtitle = "") {
  ggtitle(bquote(atop(.(title), atop(.(subtitle)))))
}

theme_custom = function(base_size = 16) {
  bg_color = "#f4f4f4"
  bg_rect = element_rect(fill = bg_color, color = bg_color)

  theme_bw(base_size) +
    theme(plot.background = bg_rect,
          panel.background = bg_rect,
          legend.background = bg_rect,
          # panel.grid.major = element_blank(), 
          panel.grid.minor = element_blank(),
          # panel.background = element_blank(), 
          axis.line = element_line(colour = "black"),      
          panel.grid.major = element_line(colour = "grey80", size = 0.25))
          # panel.grid.minor = element_line(colour = "grey90", size = 0.25))
}

# Export settings
w = 640
h = 420


transact = query("SELECT t1.transact_id,
                   t1.timestamp,
                   t1.provider,
                   t2.id, 
                   t2.trade_date,
                   t2.tid,
                   t2.price, t2.amount, t2.side
                   FROM 
                   transactpull as t1
                   INNER JOIN
                   'transaction' as t2
                   ON t1.transact_id = t2.transact_id
                   ORDER BY t1.transact_id, t1.timestamp, 
                            t2.trade_date, t2.tid
                   ")

# Remove duplicate observations
t2 = transact %>% 
     distinct(timestamp, provider, trade_date, price, amount, side)

# Convert to date
t2$timestamp = as.POSIXct(t2$timestamp)
t2$trade_date = as.POSIXct(t2$trade_date)

t2$hourid = format(t2$trade_date, format = "%H")
is.character(t2$hourid)
head(t2$hourid)

t3 = t2 %>% 
     group_by(hourid) %>%
     summarize(n=n())

# Number of transaction per hour
ggplot(data=t3, aes(x=hourid, y=n)) +
    geom_bar(stat="identity", alpha=0.5) + 
    ggtitle("Number of Transaction") +
    theme_custom() 
    add_credits()

price = query("SELECT * from price
               ORDER BY timestamp")

# Remove duplicate observations
p2 = price %>% 
     mutate(spread=ask - bid)
p2$timestamp = as.POSIXct(p2$timestamp)
p2$hourid = format(p2$timestamp, format = "%H")

# Graph spread over time
ggplot(p2, aes(x=timestamp, y=spread, color=provider)) +
    geom_point(shape=1, alpha=0.5) + 
    stat_smooth() + 
    xlab("") + ylab("Spread") +
    ggtitle("Bid-Ask Spread over Time") +
    theme_custom() +
    theme(legend.position='bottom')
    add_credits()

# Graph spread by hours
ggplot(p2, aes(x=as.numeric(hourid), y=spread, color=provider)) +
    geom_point(shape=1, alpha=0.5) + 
    scale_shape_manual(values=c(1,2)) +
    stat_smooth() + 
    ggtitle("Spread over Time") +
    theme_custom() 
    add_credits()



# Graph price over time
ggplot(p2, aes(x=timestamp, y=last, color=provider)) +
    geom_line() + 
    ggtitle("Price over Time") +
    theme_custom() 
    add_credits()

# end #