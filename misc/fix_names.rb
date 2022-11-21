Dir.foreach("../json/journals") do |d|
  next if d.match(/^\./)
  unless d.match(/-/)
    `mv ../json/journals/#{d} ../json/journals/#{d[0..-6]}-meat.json`
  end
end

exit
Dir.foreach("../grobid") do |dir|
  next if dir.match(/^\./)
  Dir.foreach("../grobid/#{dir}") do |d|
    next if d.match(/^\./)
    unless d.match(/.json$/)
      `mv ../grobid/#{dir}/#{d} ../grobid/#{dir}/#{d}.json`
    end
  end
end

exit
Dir.foreach("../pdfs") do |dir|
  next if dir.match(/^\./)
  Dir.foreach("../pdfs/#{dir}") do |d|
    next if d.match(/^\./)
    puts "#{dir} => #{d}"
    `mv ../pdfs/#{dir}/#{d} ../pdfs/#{dir}/#{d.gsub("_","-")}`
  end
end
